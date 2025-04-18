from serpapi import GoogleSearch


async def search_web(query: str) -> str:
    """
    Perform a web search using SerpAPI and return the search results.

    Args:
        query (str): The search query.

    Returns:
        str: The search results in HTML format.
    """

    params = {
        "engine": "google",
        "q": query,
        "api_key": "YOUR_SERPAPI_KEY",
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    if "error" in results:
        return f"Error: {results['error']}"

    return results
