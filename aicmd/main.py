import os
import platform
import sys
import subprocess
from dotenv import load_dotenv
from .config import settings, Colors
from .openai_api import generate_shell_command, is_command_safe
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
        print(colorize("The generated command was not considered safe to execute. Aborted.", Colors.FAIL))

if __name__ == "__main__":
    main()
