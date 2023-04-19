import json
import importlib.resources

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def load_settings():
    with importlib.resources.open_text('aicmd', 'settings.json') as settings_file:
        settings = json.load(settings_file)
    return settings

settings = load_settings()