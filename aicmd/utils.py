import subprocess
from .config import settings, Colors

def colorize(text, color):
    if settings["use_colors"]:
        return f"{color}{text}{Colors.ENDC}"
    return text

def execute_command(shell_command, operating_system):
    if operating_system == 'Windows':
        result = subprocess.run(shell_command, shell=True, check=True, capture_output=True, text=True)
    else:
        #try catch against non-zero exit codes and print stderr
        try:
            result = subprocess.run(shell_command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(colorize(f"{e.stderr}", Colors.FAIL))
            return e.stderr
    return result