from langchain_community.tools.tavily_search import TavilySearchResults
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
        max_results=5,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=True,
        include_images=True,
        # include_domains=[...],
        # exclude_domains=[...],
        # name="...",            # overwrite default tool name
        # description="...",     # overwrite default tool description
        # args_schema=...,       # overwrite default args_schema: BaseModel
    )

    query = """
    Bash scripting tasks for system administration, DevOps, and programming:
    1. System monitoring and management
    2. File operations and text processing
    3. Network configuration and diagnostics
    4. User and permission management
    5. Package installation and updates
    6. Backup and recovery
    7. Log analysis and reporting
    8. CI/CD pipeline automation
    9. Container and virtualization management
    10. Version control operations
    11. Database administration
    12. Web server configuration
    13. Security and encryption
    14. Cloud infrastructure management
    15. Automated testing and deployment
    """
    print(f"Searching for: {query}")

    try:
        search_results = search_tool.invoke({"query": query})
        print(search_results)

        seeds = []
        for result in search_results:
            if isinstance(result, dict) and 'title' in result:
                seeds.append(result['title'])
            elif isinstance(result, str):
                seeds.append(result)

        return seeds

    except Exception as e:
        print(f"Error occurred while searching: {e}")
        return []


def run_seed_research():
    seeds = search_seeds()
    print(f"Found {len(seeds)} seeds.")
    if seeds:
        os.makedirs('data', exist_ok=True)
        with open('data/seeds.json', 'w') as f:
            json.dump(seeds, f, indent=4)
        print("Seed research complete. Seeds saved to data/seeds.json")
    else:
        print("No seeds found. Debugging information:")
        print(
            f"TAVILY_API_KEY set: {'Yes' if os.getenv('TAVILY_API_KEY') else 'No'}")
        print("Please check your internet connection and Tavily API key.")
    return seeds


if __name__ == "__main__":
    run_seed_research()
