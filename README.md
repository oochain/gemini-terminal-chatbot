# Gemini Terminal Chat

A simple terminal-based chat interface for Google's Gemini AI with
file attachment support.

## Setup

1. Install dependencies:

    ```bash
    pip install -r requirements.txt
    # or if using uv:
    uv pip install -e .
    ```

2. Set up your API key:

    ```bash
    cp .env.bak .env
    # Edit .env and add your Gemini API key
    ```

## Usage

Run the chat:

```bash
python main.py
# or if using uv:
uv run main.py
```

### Commands

- `exit` - End conversation
- `send` - Send multi-line message
- `file: path/to/file` - Attach a file for context

## License

MIT
