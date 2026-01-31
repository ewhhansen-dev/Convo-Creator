from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTextEdit, QLabel, QMessageBox, QApplication)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from src.audio_capture import AudioRecorder
from src.transcriber import AudioTranscriber
from src.session_manager import SessionManager
import pyperclip
import os
import shutil

class TranscriberThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, transcriber, audio_path):
        super().__init__()
        self.transcriber = transcriber
        self.audio_path = audio_path

    def run(self):
        try:
            text = self.transcriber.transcribe(self.audio_path)
            self.finished.emit(text)
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setWindowTitle(config['app']['name'])
        self.resize(600, 800)

        # Initialize Backend Components
        self.audio_recorder = AudioRecorder(
            sample_rate=config['audio']['sample_rate'],
            channels=config['audio']['channels']
        )
        self.transcriber = AudioTranscriber(
            model_size=config['transcription']['model_size'],
            device=config['transcription']['device'],
            compute_type=config['transcription']['compute_type']
        )
        self.session_manager = SessionManager(
            storage_path=config['storage']['base_path']
        )

        self.is_recording = False
        self.temp_audio_path = config['audio']['temp_filename']

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Status Label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # Text Area
        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText("Transcription will appear here...")
        layout.addWidget(self.text_area)

        # Buttons Layout
        btn_layout = QHBoxLayout()

        self.record_btn = QPushButton("Record")
        self.record_btn.clicked.connect(self.toggle_recording)
        self.record_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        btn_layout.addWidget(self.record_btn)

        self.copy_btn = QPushButton("Copy to Clipboard")
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        btn_layout.addWidget(self.copy_btn)

        layout.addLayout(btn_layout)

        # AI Actions (Placeholder)
        ai_layout = QHBoxLayout()
        self.ai_btn = QPushButton("AI Refine (Coming Soon)")
        self.ai_btn.setEnabled(False)
        ai_layout.addWidget(self.ai_btn)
        layout.addLayout(ai_layout)

    def toggle_recording(self):
        if not self.is_recording:
            # Start Recording
            try:
                self.audio_recorder.start_recording()
                self.is_recording = True
                self.record_btn.setText("Stop")
                self.record_btn.setStyleSheet("background-color: #f44336; color: white; padding: 10px;")
                self.status_label.setText("Recording...")
                self.text_area.clear()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to start recording: {e}")
        else:
            # Stop Recording
            try:
                self.audio_recorder.stop_recording(self.temp_audio_path)
                self.is_recording = False
                self.record_btn.setText("Record")
                self.record_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
                self.status_label.setText("Transcribing...")
                self.start_transcription()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to stop recording: {e}")
                self.status_label.setText("Error")

    def start_transcription(self):
        self.thread = TranscriberThread(self.transcriber, self.temp_audio_path)
        self.thread.finished.connect(self.on_transcription_finished)
        self.thread.error.connect(self.on_transcription_error)
        self.thread.start()

    def on_transcription_finished(self, text):
        self.text_area.setText(text)
        self.status_label.setText("Ready")

        # Save to session log
        saved_path = self.session_manager.save_transcription(text)
        if saved_path:
            self.statusBar().showMessage(f"Saved to {saved_path}", 3000)

        # Optional: Auto-copy
        # pyperclip.copy(text)

    def on_transcription_error(self, error_msg):
        self.status_label.setText("Error during transcription")
        QMessageBox.warning(self, "Transcription Error", error_msg)

    def copy_to_clipboard(self):
        text = self.text_area.toPlainText()
        if text:
            pyperclip.copy(text)
            self.status_label.setText("Copied to clipboard!")
            # Reset status after 2 seconds
            # (In a real app, use QTimer)
