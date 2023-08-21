import sys
import os
import subprocess
from enum import Enum
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from shell_ai.config import load_config

def main():
    """
        Required environment variables:
        - OPENAI_API_KEY: Your OpenAI API key. You can find this on https://beta.openai.com/account/api-keys

        Allowed envionment variables:
        - OPENAI_MODEL: The name of the OpenAI model to use. Defaults to `gpt-3.5-turbo`.
        - SHAI_SUGGESTION_COUNT: The number of suggestions to generate. Defaults to 3.

    """

    # Load env configuration
    loaded_config = load_config()
    # Load keys of the configuration into environment variables
    for key, value in loaded_config.items():
        os.environ[key] = value
    
    if os.environ.get("OPENAI_API_KEY") is None:
        print("Please set the OPENAI_API_KEY environment variable to your OpenAI API key.")
        sys.exit(1)

    OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
    SHAI_SUGGESTION_COUNT = int(os.environ.get("SHAI_SUGGESTION_COUNT", 3))
    # End loading configuration

    chat = ChatOpenAI(model_name=OPENAI_MODEL, n=SHAI_SUGGESTION_COUNT)
    system_message = SystemMessage(content=
        """You are an expert at using shell commands. Only provide a single executable line of shell code as output. Never output any text before or after the shell code, as the output will be directly executed in a shell. You're allowed to chain commands like `ls | grep .txt`."""
    )

    def get_suggestions(prompt):
        response = chat.generate(messages=[[system_message, HumanMessage(content=f"Here's what I'm trying to do: {prompt}")]])
        return [msgs.message.content for msgs in response.generations[0]]

    # Consume all arguments after the script name as a single sentence
    prompt = ' '.join(sys.argv[1:])

    if prompt:

        class SelectSystemOptions(Enum):
            OPT_GEN_SUGGESTIONS = "Generate new suggestions"
            OPT_DISMISS = "Dismiss"

        
        while True:
            options = get_suggestions(prompt)
            options.append(SelectSystemOptions.OPT_GEN_SUGGESTIONS.value)
            options.append(SelectSystemOptions.OPT_DISMISS.value)
            choices = [Choice(value=option, name=option) for option in options]
            
            selection = inquirer.select(
                message="Select a command:",
                choices=choices
            ).execute()
        
            try:
                if selection == SelectSystemOptions.OPT_DISMISS.value:
                    sys.exit(0)
                elif selection == SelectSystemOptions.OPT_GEN_SUGGESTIONS.value:
                    continue
                subprocess.run(selection, shell=True, check=True)
                break
            except subprocess.CalledProcessError as e:
                print(f"Error executing command: {e}")
                break
    else:
        print("Describe what you want to do as a single sentence. `shai <sentence>`")

if __name__ == "__main__":
    main()
