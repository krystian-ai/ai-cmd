import os
import platform
import sys

from dotenv import load_dotenv
from .config import settings, Colors
from .openai_api import generate_shell_command, is_command_safe, get_result_analysis
from .utils import colorize, execute_command


def load_env_vars():
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")


def read_config():
    return settings["command_execution_confirmation"], settings["security_check"], settings["openai_model_config"]


def recognize_operating_system():
    return platform.system()


def read_user_command():
    return " ".join(sys.argv[1:])


def print_and_check_security(shell_command, security_check, openai_api_key, openai_model_config):
    print(colorize(f"EXECUTEING: {shell_command}", Colors.OKGREEN))

    if security_check:
        command_safety_analysis = is_command_safe(shell_command, openai_api_key, openai_model_config)
        if command_safety_analysis.startswith("safe"):
            command_safe = True
        else:
            command_safe = False
            print(colorize(f"WARNING: {command_safety_analysis}", Colors.WARNING))
    else:
        command_safe = True

    if command_safe:
        # Print shell command and ask user for confirmation
        print(colorize(f"Generated shell command: {shell_command}", Colors.OKGREEN))
        if command_execution_confirmation:
            if command_execution_confirmation:
                user_input = input(colorize("Do you want to execute this command? (y/n): ", Colors.OKCYAN)).lower()
            if user_input == 'y':
                # Execute command in shell
                if operating_system == 'Windows':
                    subprocess.run(shell_command, shell=True, check=True)
                else:
                    subprocess.run(shell_command, shell=True, executable='/bin/bash', check=True)
            else:
                print(colorize("Command execution aborted.", Colors.WARNING))
        else:
            # Execute command without asking for confirmation
            if operating_system == 'Windows':
                subprocess.run(shell_command, shell=True, check=True)
            else:
                subprocess.run(shell_command, shell=True, executable='/bin/bash', check=True)
    else:
        print(colorize("Command execution aborted.", Colors.FAIL))


if __name__ == "__main__":
    main()
