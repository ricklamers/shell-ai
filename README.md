# Shell-AI: Your Intelligent Command-Line Companion

Shell-AI (`shai`) is a CLI utility that brings the power of natural language understanding to your command line. Simply input what you want to do in natural language, and `shai` will suggest single-line commands that achieve your intent. Under the hood, Shell-AI leverages the [LangChain](https://github.com/langchain-ai/langchain) for LLM use and builds on the excellent [InquirerPy](https://github.com/kazhala/InquirerPy) for the interactive CLI.

![demo-shell-ai](https://github.com/ricklamers/shell-ai/assets/1309307/b4057165-5c23-46d4-b68e-00915b738dc3)

## Installation

You can install Shell-AI directly from PyPI using pip:

```bash
pip install shell-ai
```

After installation, you can invoke the utility using the `shai` command.

## Usage

To use Shell-AI, open your terminal and type:

```bash
shai run terraform dry run thingy
```

Shell-AI will then suggest 3 commands to fulfill your request:
- `terraform plan`
- `terraform plan -input=false`
- `terraform plan`

## Features

- **Natural Language Input**: Describe what you want to do in plain English (or other supported languages).
- **Command Suggestions**: Get single-line command suggestions that accomplish what you asked for.
- **Cross-Platform**: Works on Linux, macOS, and Windows.

## Configuration
### Environment Variables

1. **`OPENAI_API_KEY`**: Required. Set this environment variable to your OpenAI API key. You can find it on your [OpenAI Dashboard](https://beta.openai.com/account/api-keys).

### Optional Variables

1. **`OPENAI_MODEL`**: Defaults to `gpt-3.5-turbo`. You can set it to another OpenAI model if desired.
2. **`SHAI_SUGGESTION_COUNT`**: Defaults to 3. You can set it to specify the number of suggestions to generate.

### Configuration File

Alternatively, you can store these variables in a JSON configuration file:

- For Linux/macOS: Create a file called `config.json` under `~/.config/shell-ai/`
- For Windows: Create a file called `config.json` under `%APPDATA%\shell-ai\`

Example `config.json`:

```json
{
  "OPENAI_API_KEY": "your_openai_api_key_here",
  "OPENAI_MODEL": "gpt-3.5-turbo",
  "SHAI_SUGGESTION_COUNT": 3
}
```

The application will read from this file if it exists, overriding any existing environment variables.

Run the application after setting these configurations.


## Contributing

This implementation can be made much smarter! Contribute your ideas as Pull Requests and make AI Shell better for everyone.

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

Shell-AI is licensed under the MIT License. See [LICENSE](LICENSE) for details.
