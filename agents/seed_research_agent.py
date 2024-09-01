import os
import json
from logs.generation_logs import logger
from tools.search_tool import search_seeds


def run_seed_research():
    seeds = search_seeds()
    if seeds:
        # Save the seeds to a file for later use
        os.makedirs('data', exist_ok=True)
        with open('data/seeds.json', 'w') as f:
            json.dump(seeds, f, indent=4)

        for seed in seeds:
            logger.log_seed(seed)

        print("Seed research complete. Seeds saved to data/seeds.json")
    else:
        print("No seeds found.")

    return seeds


if __name__ == "__main__":
    seeds = run_seed_research()
    print(f"Generated seeds: {seeds}")
