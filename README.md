# AI-Shell: Your Intelligent Command-Line Companion

AI-Shell (`ais`) is a CLI utility that brings the power of natural language understanding to your command line. Simply input what you want to do in natural language, and `ais` will suggest single-line commands that achieve your intent. Under the hood, AI-Shell leverages the [LangChain](https://github.com/langchain-ai/langchain) for LLM use and builds on the excellent [InquirerPy](https://github.com/kazhala/InquirerPy) for the interactive CLI.

## Installation

You can install AI-Shell directly from PyPI using pip:

```bash
pip install ai-shell
```

After installation, you can invoke the utility using the `ais` command.

## Usage

To use AI-Shell, open your terminal and type:

```bash
ais run terraform dry run thingy
```

AI-Shell will then suggest 3 commands to fulfill your request:
- `terraform plan`
- `terraform plan -input=false`
- `terraform plan`

## Features

- **Natural Language Input**: Describe what you want to do in plain English (or other supported languages).
- **Command Suggestions**: Get single-line command suggestions that accomplish what you asked for.
- **Cross-Platform**: Works on Linux, macOS, and Windows.

## Contributing

This implementation can be made much smarter! Contribute your ideas as Pull Requests and make AI Shell better for everyone.

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

AI-Shell is licensed under the MIT License. See [LICENSE](LICENSE) for details.
