import os
import platform
import sys

from dotenv import load_dotenv
from .config import settings, Colors
from .openai_api import generate_shell_command, is_command_safe, get_result_analysis  # Add generate_message_prompt
from .utils import colorize, execute_command

def main():
    # Load environment variables
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Read the configuration
    command_execution_confirmation = settings["command_execution_confirmation"]
    security_check = settings["security_check"]

    # Set up OpenAI engine with parameters
    openai_model_config = settings["openai_model_config"]

    # Read and recognize the operating system
    operating_system = platform.system()

    # Read the command from the command prompt
    user_command = " ".join(sys.argv[1:])

    # Generate shell command using OpenAI API
    shell_command = generate_shell_command(user_command, openai_api_key, openai_model_config)

    # Print shell command
    print(colorize(f"EXECUTEING: {shell_command}", Colors.OKGREEN))

    # Check if command is safe
    if security_check:
        command_safety_analysis = is_command_safe(shell_command, openai_api_key, openai_model_config) 
        # Write if command_safety_analysis starts with a word "safe" then command_safe = True otherwize false
        if command_safety_analysis.startswith("safe"):
            command_safe = True
        else:
            command_safe = False
            print(colorize(f"WARNING: {command_safety_analysis}", Colors.WARNING))
    else:
        command_safe = True

    # Ask user for confirmation if security check is enabled or command_execution_confirmation is enabled
    if command_execution_confirmation or not command_safe:
        user_input = input(colorize("Do you want to execute this command? (y/n): ", Colors.OKCYAN)).lower()
        command_execution_confirmation = user_input == 'y'
    else:
        command_execution_confirmation = True

    if command_execution_confirmation:
        command_execution_result = execute_command(shell_command, operating_system)
        command_execution_analysis = get_result_analysis(command_execution_result, openai_api_key, openai_model_config)
        if "FAILED" not in command_execution_analysis:
            print(colorize(f"{command_execution_result.stdout}", Colors.OKBLUE))
            analysis_color = Colors.OKCYAN
        else:
            analysis_color = Colors.FAIL
        print(colorize(f"{command_execution_analysis}", analysis_color))
    else:
        print(colorize("Command execution aborted.", Colors.FAIL))

if __name__ == "__main__":
    main()
