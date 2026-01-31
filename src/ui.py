import flet as ft
import pyperclip

class DictationUI:
    def __init__(self, on_record_toggle=None):
        self.on_record_toggle = on_record_toggle
        self.page = None
        self.txt_output = None
        self.btn_record = None
        self.status_text = None
        self.is_recording = False

    def main(self, page: ft.Page):
        self.page = page
        page.title = "Convo-Creator"
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.theme_mode = ft.ThemeMode.DARK

        # Components
        self.status_text = ft.Text("Ready", color=ft.Colors.GREY)

        self.txt_output = ft.TextField(
            multiline=True,
            min_lines=10,
            max_lines=20,
            text_size=16,
            expand=True,
            border_color=ft.Colors.GREY_800
        )

        self.btn_record = ft.FloatingActionButton(
            icon=ft.icons.MIC,
            bgcolor=ft.Colors.BLUE,
            on_click=self._handle_record_click
        )

        btn_copy = ft.IconButton(
            icon=ft.icons.COPY,
            tooltip="Copy to Clipboard",
            on_click=lambda e: self.copy_to_clipboard()
        )

        btn_clear = ft.IconButton(
            icon=ft.icons.CLEAR_ALL,
            tooltip="Clear Text",
            on_click=lambda e: self.clear_text()
        )

        # Layout
        toolbar = ft.Row([
            ft.Text("Dictation Station", size=20, weight=ft.FontWeight.BOLD),
            ft.Container(expand=True),
            btn_copy,
            btn_clear
        ])

        page.add(
            toolbar,
            self.status_text,
            self.txt_output,
            ft.Container(height=20),
            ft.Row([self.btn_record], alignment=ft.MainAxisAlignment.CENTER)
        )

    def _handle_record_click(self, e):
        if self.on_record_toggle:
            self.on_record_toggle()

    def set_recording_state(self, is_recording):
        self.is_recording = is_recording
        if self.page:
            if is_recording:
                self.btn_record.icon = ft.icons.STOP
                self.btn_record.bgcolor = ft.Colors.RED
                self.status_text.value = "Recording..."
                self.status_text.color = ft.Colors.RED
            else:
                self.btn_record.icon = ft.icons.MIC
                self.btn_record.bgcolor = ft.Colors.BLUE
                self.status_text.value = "Processing..."
                self.status_text.color = ft.Colors.YELLOW
            self.page.update()

    def update_text(self, new_text):
        if self.page and self.txt_output:
            current = self.txt_output.value or ""
            # Append with a newline if there's existing text
            if current:
                self.txt_output.value = current + "\n" + new_text
            else:
                self.txt_output.value = new_text

            self.status_text.value = "Ready"
            self.status_text.color = ft.Colors.GREEN
            self.page.update()

    def copy_to_clipboard(self):
        if self.txt_output and self.txt_output.value:
            pyperclip.copy(self.txt_output.value)
            self.page.show_snack_bar(ft.SnackBar(ft.Text("Copied to clipboard!")))

    def clear_text(self):
        if self.txt_output:
            self.txt_output.value = ""
            self.page.update()
