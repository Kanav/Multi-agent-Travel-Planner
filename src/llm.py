import os
from langchain_openai import ChatOpenAI


def get_llm(model_name: str = "gpt-5.2", temperature: float = 0.2):
    """Initialize and return a ChatOpenAI model using the OpenAI API key from environment variables."""
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY environment variable not found. Please set it before using the LLM."
        )

    llm = ChatOpenAI(
        model=model_name,
        temperature=temperature,
        openai_api_key=api_key
    )

    return llm


if __name__ == "__main__":
    llm = get_llm()
    print(f"LLM model '{llm.model_name}' initialized successfully.")
