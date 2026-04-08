import os


def setup_tavily_api_key():
    """Retrieve the Tavily API key from environment variables and verify its presence."""
    api_key = os.environ.get("TAVILY_API_KEY")

    if not api_key:
        print("Error: TAVILY_API_KEY environment variable not found.")
        print("Please set it using 'export TAVILY_API_KEY=your_api_key' or in your .env file.")
        return None

    print("Tavily API key successfully loaded from environment variables.")
    return api_key


if __name__ == "__main__":
    setup_tavily_api_key()
