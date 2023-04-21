import os
import platform
import sys
import subprocess
from dotenv import load_dotenv
from .config import settings, Colors
from .openai_api import generate_shell_command, is_command_safe, generate_message_prompt  # Add generate_message_prompt
from .utils import colorize

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

    # Check if command is safe
    if security_check:
        command_safe = is_command_safe(shell_command, openai_api_key, openai_model_config)
    else:
        command_safe = True

    if command_safe:
        # Print shell command
        print(colorize(f"Generated shell command: {shell_command}", Colors.OKGREEN))

        # Ask user for confirmation if security check is enabled or command_execution_confirmation is enabled
        if security_check or command_execution_confirmation:
            user_input = input(colorize("Do you want to execute this command? (y/n): ", Colors.OKCYAN)).lower()
            execute_command = user_input == 'y'
        else:
            execute_command = True

        if execute_command:
            # Execute command in shell and capture output
            if operating_system == 'Windows':
                result = subprocess.run(shell_command, shell=True, check=True, capture_output=True, text=True)
            else:
                result = subprocess.run(shell_command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
            
            # Send output to OpenAI API
            message_prompt = generate_message_prompt(result.stdout, openai_api_key, openai_model_config)
            print(colorize(f"OpenAI prompt: {message_prompt}", Colors.OKCYAN))

        else:
            print(colorize("Command execution aborted.", Colors.WARNING))
    else:
        print(colorize("The generated command was not considered safe to execute. Aborted.", Colors.FAIL))

if __name__ == "__main__":
    main()
