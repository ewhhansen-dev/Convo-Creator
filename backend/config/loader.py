import toml
import os
from backend.config.models import AppConfig, ButtonMap

SETTINGS_PATH = "config/settings.toml"
BUTTON_MAP_PATH = "config/button_map.toml"

def load_settings() -> AppConfig:
    if not os.path.exists(SETTINGS_PATH):
        print(f">>> Config not found at {SETTINGS_PATH}, using defaults.")
        return AppConfig()

    try:
        data = toml.load(SETTINGS_PATH)
        return AppConfig(**data)
    except Exception as e:
        print(f"Error loading settings: {e}")
        return AppConfig()

def load_button_map() -> ButtonMap:
    if not os.path.exists(BUTTON_MAP_PATH):
        return ButtonMap()

    try:
        data = toml.load(BUTTON_MAP_PATH)
        # Assuming toml structure is { "buttons": [ ... ] }
        return ButtonMap(**data)
    except Exception as e:
        print(f"Error loading button map: {e}")
        return ButtonMap()
