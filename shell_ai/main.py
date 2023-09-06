import os
import subprocess
import sys
import textwrap
from enum import Enum

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from shell_ai.config import load_config


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
        content="""You are an expert at using shell commands. Only provide a single executable line of shell code as output. Never output any text before or after the shell code, as the output will be directly executed in a shell. You're allowed to chain commands like `ls | grep .txt`."""
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
        return [msgs.message.content for msgs in response.generations[0]]

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

            selection = inquirer.select(
                message="Select a command:", choices=choices
            ).execute()

            try:
                if selection == SelectSystemOptions.OPT_DISMISS.value:
                    sys.exit(0)
                elif selection == SelectSystemOptions.OPT_GEN_SUGGESTIONS.value:
                    continue
                user_command = inquirer.text(
                    message="Confirm:", default=selection
                ).execute()
                subprocess.run(user_command, shell=True, check=True)
                break
            except subprocess.CalledProcessError as e:
                print(f"Error executing command: {e}")
                break
    else:
        print("Describe what you want to do as a single sentence. `shai <sentence>`")


if __name__ == "__main__":
    main()
