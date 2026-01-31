import sys
import yaml
import os
from PyQt6.QtWidgets import QApplication
from src.gui import MainWindow

def load_config(config_path="config/settings.yaml"):
    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}")
        return {}

    with open(config_path, "r") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(f"Error parsing config: {exc}")
            return {}

def main():
    # Load Configuration
    config = load_config()
    if not config:
        print("Failed to load configuration. Exiting.")
        sys.exit(1)

    app = QApplication(sys.argv)

    # Set Theme (Simple Dark Mode tweak if config says so)
    if config.get('ui', {}).get('theme') == 'Dark':
        app.setStyle("Fusion")

    window = MainWindow(config)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
