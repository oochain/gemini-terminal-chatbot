from dotenv import load_dotenv
import os
from colorama import init, Fore, Style, Back
from google import genai
from rich.console import Console
from rich.markdown import Markdown

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    print(f"{Fore.RED}Error: API_KEY not found in .env file{Style.RESET_ALL}")
    print(f"{Fore.RED}rename .env.bak to .env and update your API Key{Style.RESET_ALL}")
    raise

console = Console()
HISTORY_FILE = "chat_history.md"
GEMINI_MODE = "gemini-2.0-flash"


def display_readme(readme_content):
    """Displays Markdown content using rich."""
    markdown = Markdown(readme_content)
    console.print(markdown)


def load_history(filepath=HISTORY_FILE):
    try:
        with open(filepath, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def save_history(user_input, gemini_response, filepath=HISTORY_FILE):
    with open(filepath, "a") as f:
        f.write(f"\n\n**You:**\n\n{user_input}\n\n**Gemini:**\n\n{gemini_response}\n")


def handle_file_upload(client, filepath):
    """Handle file upload to Gemini API."""
    try:
        # Verify file exists
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        # Upload file
        file_obj = client.files.upload(file=filepath)
        return file_obj
    except Exception as e:
        raise Exception(f"Error uploading file: {str(e)}")


def main():
    # Initialize colorama for cross-platform color support
    init()

    # Initialize the client
    client = genai.Client(api_key=API_KEY)

    # Create a new chat session
    chat = client.chats.create(model=GEMINI_MODE)

    # Load and display history
    history = load_history()
    if history:
        console.print(Markdown(history))

    # Welcome message with fancy formatting
    print(
        f"\n{Back.BLUE}{Fore.WHITE} Welcome to Enhanced Gemini Chatbot! {Style.RESET_ALL}"
    )
    print(f"{Fore.CYAN}Commands:")
    print(f"• Type '{Fore.YELLOW}exit{Fore.CYAN}' to end the conversation")
    print(f"• Type '{Fore.YELLOW}send{Fore.CYAN}' to send your multi-line message")
    print(f"• Type '{Fore.YELLOW}file: path/to/file{Fore.CYAN}' to attach a file")
    print(f"• After attaching a file, all questions can reference it{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'-' * 50}{Style.RESET_ALL}\n")

    # Store the currently attached file
    current_file = None

    # Main chat loop
    while True:
        print(f"{Fore.GREEN}You: {Style.RESET_ALL}", end="")
        user_lines = []

        while True:
            try:
                line = input()

                # Handle exit command
                if line.strip() == "exit":
                    print(f"\n{Back.GREEN}{Fore.BLACK} Goodbye! {Style.RESET_ALL}\n")
                    return

                # Handle file attachment
                elif line.strip().startswith("file:"):
                    filepath = line.strip()[5:].strip()  # Remove 'file:' and whitespace
                    try:
                        current_file = handle_file_upload(client, filepath)
                        print(
                            f"{Fore.GREEN}File attached successfully: {filepath}{Style.RESET_ALL}"
                        )
                    except Exception as e:
                        print(
                            f"{Fore.RED}Error attaching file: {str(e)}{Style.RESET_ALL}"
                        )
                    break

                # Regular send command
                elif line.strip() == "send":
                    break

                # Handle regular send command
                elif line.strip() == "send":
                    break

                user_lines.append(line)

            except (KeyboardInterrupt, EOFError):
                print(f"\n{Back.RED}{Fore.WHITE} Chat terminated {Style.RESET_ALL}\n")
                return

        user_input = "\n".join(user_lines)

        # Skip empty messages
        if not user_input.strip():
            continue

        # Handle chat messages
        if user_input and not user_input.startswith("file:"):
            try:
                if current_file:
                    # If there's an attached file, include it in the context
                    response = client.models.generate_content(
                        model="gemini-2.0-flash", contents=[user_input, current_file]
                    )
                else:
                    # Regular chat without file context
                    response = chat.send_message(user_input)

                print(f"\n{Fore.BLUE}Gemini:{Style.RESET_ALL}")
                display_readme(response.text)
                print(f"\n{Fore.MAGENTA}{'-' * 50}{Style.RESET_ALL}\n")
                save_history(user_input, response.text)
            except Exception as e:
                print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}\n")
                print(f"{Fore.MAGENTA}{'-' * 50}{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
