import json
import importlib.resources

def load_settings():
    with importlib.resources.open_text('aicmd', 'settings.json') as settings_file:
        settings = json.load(settings_file)
    return settings

settings = load_settings()