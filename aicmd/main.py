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

    return command_safe


def user_confirmation(command_execution_confirmation, command_safe):
    if command_execution_confirmation or not command_safe:
        user_input = input(colorize("Do you want to execute this command? (y/n): ", Colors.OKCYAN)).lower()
        command_execution_confirmation = user_input == 'y'
    else:
        command_execution_confirmation = True

    return command_execution_confirmation


def execute_and_analyze(shell_command, operating_system, openai_api_key, openai_model_config):
    command_execution_result = execute_command(shell_command, operating_system)
    command_execution_analysis = get_result_analysis(command_execution_result, openai_api_key, openai_model_config)
    if "FAILED" not in command_execution_analysis:
        print(colorize(f"{command_execution_result.stdout}", Colors.OKBLUE))
        analysis_color = Colors.OKCYAN
    else:
        analysis_color = Colors.FAIL
    print(colorize(f"{command_execution_analysis}", analysis_color))


def main():
    openai_api_key = load_env_vars()
    command_execution_confirmation, security_check, openai_model_config = read_config()
    operating_system = recognize_operating_system()
    user_command = read_user_command()

    shell_command = generate_shell_command(user_command, openai_api_key, openai_model_config)

    command_safe = print_and_check_security(shell_command, security_check, openai_api_key, openai_model_config)

    command_execution_confirmation = user_confirmation(command_execution_confirmation, command_safe)

    if command_execution_confirmation:
        execute_and_analyze(shell_command, operating_system, openai_api_key, openai_model_config)
    else:
        print(colorize("Command execution aborted.", Colors.FAIL))


if __name__ == "__main__":
    main()
