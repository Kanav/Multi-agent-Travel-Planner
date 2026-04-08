# Create Internet Search vis TavilySearch
from langchain_tavily import TavilySearch

internet_search = TavilySearch(
    max_results=5,
    topic="general",
    # include_answer=False,
    # include_raw_content=False,
    include_images=True,
    include_image_descriptions=True,
    search_depth="advanced",
    # time_range="day",
    #include_domains=None,
    # exclude_domains=None
)

if __name__ == "__main__":
    query = "What is the capital of France?"
    results = internet_search.invoke(query)
    print(results)