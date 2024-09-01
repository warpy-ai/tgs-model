from langchain_community.tools.tavily_search import TavilySearchResults


def search_seeds():
    """
    Uses TavilySearchResults to fetch relevant topics related to Bash scripting from the web.
    """
    search_tool = TavilySearchResults(max_results=2)
    query = "Common tasks in Bash scripting"
    search_results = search_tool.run(query)

    seeds = [result['title']
             for result in search_results if 'Bash' in result['snippet']]
    return seeds


def run_seed_research():
    seeds = search_seeds()
    if seeds:
        with open('data/seeds.json', 'w') as f:
            json.dump(seeds, f, indent=4)
        print("Seed research complete. Seeds saved to data/seeds.json")
    else:
        print("No seeds found.")


if __name__ == "__main__":
    run_seed_research()
