# prompts.py

# Prompt to get commandline from user command
get_commandline_prompt = """
Given the user command: "{user_command}", provide the appropriate command line to execute.
"""

# Prompt to check if commandline is safe for user or the PC
check_command_safety_prompt = """
Is the following command line safe for the user and their computer?
Respond only Yes or No.
Command: {command}
"""

# Prompt to detect the type of command given by the user
detect_command_type_prompt = """
Given the user command: "{user_command}", determine the type of command (e.g., file management, data manipulation, etc.).
"""

# Prompt to generate a message to the user
generate_message_prompt = """
Generate a message for the user based on the context: "{context}".
"""
