import os


def setup_serp_api_key():
    """Retrieve the Serp API key from environment variables and verify its presence."""
    api_key = os.environ.get("SERPAPI_API_KEY")

    if not api_key:
        print("Error: SERPAPI_API_KEY environment variable not found.")
        print("Please set it using 'export SERPAPI_API_KEY=your_api_key' or in your .env file.")
        return None

    print("Serp API key successfully loaded from environment variables.")
    return api_key


if __name__ == "__main__":
    setup_serp_api_key()
