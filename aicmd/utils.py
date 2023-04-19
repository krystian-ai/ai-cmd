from .config import settings, Colors

def colorize(text, color):
    if settings["use_colors"]:
        return f"{color}{text}{Colors.ENDC}"
    return text
