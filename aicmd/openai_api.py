import openai
from .prompts import (
    get_commandline_prompt,
    check_command_safety_prompt,
)

def generate_shell_command(user_command, openai_api_key, openai_model_config):
    openai.api_key = openai_api_key

    formatted_prompt = get_commandline_prompt.format(user_command=user_command)
    response = openai.Completion.create(
        engine=openai_model_config["model_name"],
        prompt=formatted_prompt,
        max_tokens=openai_model_config["max_tokens"],
        n=1,
        stop=None,
        temperature=openai_model_config["temperature"],
    )

    shell_command = response.choices[0].text.strip()
    return shell_command

def is_command_safe(shell_command, openai_api_key, openai_model_config):
    openai.api_key = openai_api_key

    formatted_prompt = check_command_safety_prompt.format(command=shell_command)
    response = openai.Completion.create(
        engine=openai_model_config["model_name"],
        prompt=formatted_prompt,
        max_tokens=openai_model_config["max_tokens"],
        n=1,
        stop=None,
        temperature=openai_model_config["temperature"],
    )

    safety_result = response.choices[0].text.strip().lower()
    
    return safety_result == "yes"
