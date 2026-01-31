import flet as ft
import threading
import os
import pyperclip
from src.audio_capture import AudioRecorder
from src.midi_trigger import MidiHandler
from src.transcriber import Transcriber
from src.session_logger import SessionLogger
from src.ui import DictationUI

class ConvoCreatorApp:
    def __init__(self):
        self.ui = DictationUI(on_record_toggle=self.toggle_recording)
        self.recorder = AudioRecorder()
        self.logger = SessionLogger()
        self.midi = MidiHandler(callback_on_note=self.on_midi_trigger)
        self.transcriber = None # Lazy load
        self.is_transcribing = False

    def initialize_transcriber(self):
        if not self.transcriber:
            self.transcriber = Transcriber()

    def on_midi_trigger(self, note):
        # Called from a background thread by MidiHandler
        # We need to be careful about thread safety if updating UI directly,
        # but here we just call toggle_recording which handles logic.
        print(f"MIDI Trigger received: {note}")
        self.toggle_recording()

    def toggle_recording(self):
        # If currently transcribing, ignore toggle to prevent race conditions
        if self.is_transcribing:
            print("Ignoring toggle: currently transcribing.")
            return

        if self.recorder.recording:
            # STOP RECORDING
            self.ui.set_recording_state(False)
            wav_path = self.recorder.stop_recording()

            if wav_path:
                # Start transcription in background thread
                t = threading.Thread(target=self._process_audio, args=(wav_path,))
                t.start()
        else:
            # START RECORDING
            self.recorder.start_recording()
            self.ui.set_recording_state(True)

    def _process_audio(self, wav_path):
        self.is_transcribing = True
        try:
            # Lazy load transcriber on first use (startup speed)
            self.initialize_transcriber()

            text = self.transcriber.transcribe(wav_path)

            if text:
                # 1. Update UI
                self.ui.update_text(text)

                # 2. Copy to Clipboard
                try:
                    pyperclip.copy(text)
                except Exception as e:
                    print(f"Clipboard Error: {e}")

                # 3. Log to file
                self.logger.log_transcription(text)

            # Cleanup
            try:
                os.remove(wav_path)
            except:
                pass

        except Exception as e:
            print(f"Processing Error: {e}")
        finally:
            self.is_transcribing = False

    def run(self):
        # Start MIDI listener
        self.midi.start_listening()

        # Start UI
        ft.app(target=self.ui.main)

        # Cleanup on exit
        self.midi.stop_listening()

if __name__ == "__main__":
    app = ConvoCreatorApp()
    app.run()
