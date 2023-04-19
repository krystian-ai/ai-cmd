import json
import os

def load_settings():
    settings_file_path = os.path.join(os.path.dirname(__file__), '../settings.json')
    with open(settings_file_path) as settings_file:
        settings = json.load(settings_file)
    return settings

settings = load_settings()
