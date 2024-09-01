from langchain_community.tools import TavilySearchResults
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def search_seeds():
    """
    Uses TavilySearchResults to fetch relevant topics related to Bash scripting from the web.
    """
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        raise ValueError("TAVILY_API_KEY not found in environment variables")

    search_tool = TavilySearchResults(
        max_results=2, tavily_api_key=tavily_api_key)
    query = "Common tasks in Bash scripting"
    search_results = search_tool.invoke(query)

    seeds = []
    for result in search_results:
        if isinstance(result, dict):
            if 'title' in result and any('bash' in value.lower() for value in result.values() if isinstance(value, str)):
                seeds.append(result['title'])
        elif isinstance(result, str):
            if 'bash' in result.lower():
                seeds.append(result)

    return seeds


def run_seed_research():
    seeds = search_seeds()
    if seeds:
        os.makedirs('data', exist_ok=True)
        with open('data/seeds.json', 'w') as f:
            json.dump(seeds, f, indent=4)
        print("Seed research complete. Seeds saved to data/seeds.json")
    else:
        print("No seeds found.")
    return seeds


if __name__ == "__main__":
    run_seed_research()
