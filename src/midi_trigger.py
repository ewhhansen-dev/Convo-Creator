import mido
import threading
import time

class MidiHandler:
    """
    Listens for MIDI events to trigger callbacks.
    """
    def __init__(self, callback_on_note=None, device_name_substring=""):
        self.callback = callback_on_note
        self.device_name_substring = device_name_substring
        self.listening = False
        self._thread = None
        self._input_port = None

    def list_devices(self):
        """Returns a list of available input ports."""
        return mido.get_input_names()

    def start_listening(self):
        """Starts the listener thread."""
        if self.listening:
            return

        # Find device
        inputs = self.list_devices()
        target_device = None

        if self.device_name_substring:
            for name in inputs:
                if self.device_name_substring.lower() in name.lower():
                    target_device = name
                    break
        elif inputs:
            # Default to first available if no substring provided
            target_device = inputs[0]

        if not target_device:
            print(">>> No MIDI device found.")
            return

        print(f">>> Connecting to MIDI Device: {target_device}")

        try:
            self._input_port = mido.open_input(target_device)
            self.listening = True
            self._thread = threading.Thread(target=self._listen_loop, daemon=True)
            self._thread.start()
        except Exception as e:
            print(f"Error opening MIDI port: {e}")

    def stop_listening(self):
        self.listening = False
        if self._input_port:
            self._input_port.close()

    def _listen_loop(self):
        """Internal loop to poll for messages."""
        while self.listening:
            # Iterate through pending messages
            for msg in self._input_port.iter_pending():
                if msg.type == 'note_on' and msg.velocity > 0:
                    print(f"MIDI Note On: {msg.note}")
                    if self.callback:
                        self.callback(msg.note)
            time.sleep(0.01)
