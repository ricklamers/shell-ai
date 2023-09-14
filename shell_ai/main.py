import os
import subprocess
import sys
import textwrap
from enum import Enum
import json

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from shell_ai.config import load_config
from shell_ai.code_parser import code_parser

class SelectSystemOptions(Enum):
    OPT_GEN_SUGGESTIONS = "Generate new suggestions"
    OPT_DISMISS = "Dismiss"


class OpenAIOptions(Enum):
    openai = "openai"
    azure = "azure"


def main():
    """
    Required environment variables:
    - OPENAI_API_KEY: Your OpenAI API key. You can find this on https://beta.openai.com/account/api-keys

    Allowed envionment variables:
    - OPENAI_MODEL: The name of the OpenAI model to use. Defaults to `gpt-3.5-turbo`.
    - SHAI_SUGGESTION_COUNT: The number of suggestions to generate. Defaults to 3.
    - SHAI_SKIP_CONFIRM: Skip confirmation of the command to execute. Defaults to false. Set to `true` to skip confirmation.

    Additional required environment variables for Azure Deployments:
    - OPENAI_API_KEY: Your OpenAI API key. You can find this on https://beta.openai.com/account/api-keys
    - OPENAI_API_TYPE: "azure"
    - AZURE_API_BASE
    - AZURE_DEPLOYMENT_NAME
    """

    # Load env configuration
    loaded_config = load_config()
    # Load keys of the configuration into environment variables
    for key, value in loaded_config.items():
        os.environ[key] = str(value)

    if os.environ.get("OPENAI_API_KEY") is None:
        print(
            "Please set the OPENAI_API_KEY environment variable to your OpenAI API key."
        )
        print(
            "You can also create `config.json` under `~/.config/shell-ai/` to set the API key, see README.md for more information."
        )
        sys.exit(1)

    OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", None)
    OPENAI_ORGANIZATION = os.environ.get("OPENAI_ORGANIZATION", None)
    OPENAI_PROXY = os.environ.get("OPENAI_PROXY", None)
    SHAI_SUGGESTION_COUNT = int(os.environ.get("SHAI_SUGGESTION_COUNT", 3))

    # required configs just for azure openai deployments (faster)

    OPENAI_API_TYPE = os.environ.get("OPENAI_API_TYPE", "openai")
    OPENAI_API_VERSION = os.environ.get("OPENAI_API_VERSION", "2023-05-15")
    if OPENAI_API_TYPE not in OpenAIOptions.__members__:
        print(
            f"Your OPENAI_API_TYPE is not valid. Please choose one of {OpenAIOptions.__members__}"
        )
        sys.exit(1)
    AZURE_DEPLOYMENT_NAME = os.environ.get("AZURE_DEPLOYMENT_NAME", None)
    AZURE_API_BASE = os.environ.get("AZURE_API_BASE", None)
    if OPENAI_API_TYPE == "azure" and AZURE_DEPLOYMENT_NAME is None:
        print(
            "Please set the AZURE_DEPLOYMENT_NAME environment variable to your Azure deployment name."
        )
        sys.exit(1)
    if OPENAI_API_TYPE == "azure" and AZURE_API_BASE is None:
        print(
            "Please set the AZURE_API_BASE environment variable to your Azure API base."
        )
        sys.exit(1)

    # End loading configuration

    if OPENAI_API_TYPE == "openai":
        chat = ChatOpenAI(
            model_name=OPENAI_MODEL,
            n=SHAI_SUGGESTION_COUNT,
            openai_api_base=OPENAI_API_BASE,
            openai_organization=OPENAI_ORGANIZATION,
            openai_proxy=OPENAI_PROXY,
        )
    if OPENAI_API_TYPE == "azure":
        chat = AzureChatOpenAI(
            n=SHAI_SUGGESTION_COUNT,
            openai_api_base=AZURE_API_BASE,
            openai_api_version=OPENAI_API_VERSION,
            deployment_name=AZURE_DEPLOYMENT_NAME,
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            openai_api_type="azure",
            temperature=0,
        )

    system_message = SystemMessage(
        content="""You are an expert at using shell commands. I need you to provide a response in the format `{"command": "your_shell_command_here"}`. Only provide a single executable line of shell code as the value for the "command" key. Never output any text outside the JSON structure. The command will be directly executed in a shell. For example, if I ask to display the message 'Hello, World!', you should respond with ```json\n{"command": "echo 'Hello, World!'"}```"""
    )

    def get_suggestions(prompt):
        response = chat.generate(
            messages=[
                [
                    system_message,
                    HumanMessage(content=f"Here's what I'm trying to do: {prompt}"),
                ]
            ]
        )
        
        # Extract commands from the JSON response
        commands = []
        for msg in response.generations[0]:
            try:
                json_content = code_parser(msg.message.content)
                command_json = json.loads(json_content)
                command = command_json.get("command", "")
                if command:  # Ensure the command is not empty
                    commands.append(command)
            except json.JSONDecodeError:
                # Fallback: treat the message as a command
                commands.append(msg.message.content)


        return commands

    # Consume all arguments after the script name as a single sentence
    prompt = " ".join(sys.argv[1:])

    if prompt:
        while True:
            options = get_suggestions(prompt)
            options.append(SelectSystemOptions.OPT_GEN_SUGGESTIONS.value)
            options.append(SelectSystemOptions.OPT_DISMISS.value)

            # Get the terminal width
            terminal_width = os.get_terminal_size().columns

            # For each option for the name value of the Choice,
            # wrap the text to the terminal width
            choices = [
                Choice(
                    name=textwrap.fill(option, terminal_width, subsequent_indent="  "),
                    value=option,
                )
                for option in options
            ]
            try:
                selection = inquirer.select(
                    message="Select a command:", choices=choices
                ).execute()

                try:
                    if selection == SelectSystemOptions.OPT_DISMISS.value:
                        sys.exit(0)
                    elif selection == SelectSystemOptions.OPT_GEN_SUGGESTIONS.value:
                        continue
                    if os.environ.get("SHAI_SKIP_CONFIRM") != "true":
                        user_command = inquirer.text(
                            message="Confirm:", default=selection
                        ).execute()
                    else:
                        user_command = selection
                    subprocess.run(user_command, shell=True, check=True)
                    break
                except subprocess.CalledProcessError as e:
                    print(f"Error executing command: {e}")
                    break
            except KeyboardInterrupt:
                print("Exiting...")
                sys.exit(0)
    else:
        print("Describe what you want to do as a single sentence. `shai <sentence>`")


if __name__ == "__main__":
    main()
