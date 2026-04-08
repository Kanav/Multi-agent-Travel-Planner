import os


def setup_openai_api_key():
    """Retrieve the OpenAI API key from environment variables and verify its presence."""
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not found.")
        print("Please set it using 'export OPENAI_API_KEY=your_api_key' or in your .env file.")
        return None

    print("OpenAI API key successfully loaded from environment variables.")
    return api_key


if __name__ == "__main__":
    setup_openai_api_key()
