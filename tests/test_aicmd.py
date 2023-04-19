import unittest
from unittest.mock import patch
from aicmd.openai_api import generate_shell_command, is_command_safe

class TestAICmd(unittest.TestCase):

    @patch('aicmd.openai_api.openai.Completion.create')
    def test_generate_shell_command(self, mock_completion_create):
        user_command = "list files"
        openai_api_key = "fake_api_key"
        openai_model_config = {
            "model_name": "text-davinci-002",
            "temperature": 0.7,
            "max_tokens": 100
        }

        mock_completion_create.return_value.choices[0].text = "ls"

        shell_command = generate_shell_command(user_command, openai_api_key, openai_model_config)

        self.assertEqual(shell_command, "ls")

    @patch('aicmd.openai_api.openai.Completion.create')
    def test_is_command_safe(self, mock_completion_create):
        shell_command = "rm -rf /"
        openai_api_key = "fake_api_key"
        openai_model_config = {
            "model_name": "text-davinci-002",
            "temperature": 0.7,
            "max_tokens": 100
        }

        mock_completion_create.return_value.choices[0].text = "no"

        command_safe = is_command_safe(shell_command, openai_api_key, openai_model_config)

        self.assertFalse(command_safe)

if __name__ == "__main__":
    unittest.main()
