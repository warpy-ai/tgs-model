import os
import time
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
from logs.generation_logs import logger
from utils.rate_limiter import RateLimiter

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found in .env file")

# Initialize the model
model = ChatAnthropic(model_name="claude-3-sonnet-20240229",
                      anthropic_api_key=ANTHROPIC_API_KEY)

# Create prompt template
seed_research_prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in generating natural language commands for bash scripts."),
    ("human", """Generate a large list of natural language commands for bash scripts related to {technology}. Each command should describe a specific task or operation that can be automated using a bash script. The commands should be concise, clear, and cover a wide range of topics.

    Rules:
    1. Generate at least 200 unique commands.
    2. Each command should be a single line.
    3. Do not include numbering or categories in the output.
    4. Ensure a good mix of commands across all mentioned categories.
    5. Make sure each command is unique and not repetitive.
    6. Use natural language.
    7. Avoid compost phrase in the output, Example: "Display the current CPU usage for all processes. Generating a new Command"
    8. Use the following format:
    Display the current CPU usage for all processes
    List the top 10 memory-consuming processes
    Monitor real-time CPU load every 2 seconds
    ...

    Begin generating the commands now:""")
])

# Create chain
seed_research_chain = seed_research_prompt_template | model | StrOutputParser()


def load_existing_seeds():
    if os.path.exists('data/seeds.json'):
        with open('data/seeds.json', 'r') as f:
            return json.load(f)
    return []


def save_seeds(seeds):
    os.makedirs('data', exist_ok=True)
    with open('data/seeds.json', 'w') as f:
        json.dump(seeds, f, indent=4)


def run_seed_research():
    # Load existing seeds
    existing_seeds = load_existing_seeds()
    all_seeds = existing_seeds.copy()
    technology_counts = {}
    rate_limiter = RateLimiter(requests_per_minute=50, tokens_per_minute=40000)

    # Read the technologies list
    with open('data/technologies_list_2.txt', 'r') as file:
        technologies = [line.strip() for line in file if line.strip()]

    for technology in technologies:
        print(f"Generating commands for technology: {technology}")
        technology_counts[technology] = 0

        while technology_counts[technology] < 200:
            try:
                estimated_tokens_for_request = 100
                rate_limiter.wait(tokens=estimated_tokens_for_request)
                # Retry mechanism
                retries = 5  # Increased retries
                while retries > 0:
                    try:
                        # Generate instructions
                        response = seed_research_chain.invoke(
                            {"technology": technology})
                        break
                    except Exception as e:
                        retries -= 1
                        print(
                            f"Error generating commands for {technology}, retries left: {retries}. Error: {e}")
                        time.sleep(5)  # Wait before retrying

                if retries == 0:
                    print(
                        f"Failed to generate commands for {technology} after multiple attempts.")
                    break

                # Extract the generated instructions
                seeds = [line.strip()
                         for line in response.strip().split('\n') if line.strip()]

                for seed in seeds:
                    if seed not in all_seeds:
                        all_seeds.append(seed)
                        logger.log_seed(seed)
                        technology_counts[technology] += 1
                        if technology_counts[technology] >= 200:
                            break
                    else:
                        print(
                            f"Duplicate command found: {seed}. Generating a new command.")
                        retries = 5  # Reset retries to generate a new command

                print(
                    f"Generated {technology_counts[technology]} commands for {technology}")

            except Exception as e:
                print(f"Error generating commands for {technology}: {e}")
                break  # Break the loop if an error occurs to avoid infinite loop

        # Save seeds after processing each technology
        save_seeds(all_seeds)

    if all_seeds:
        print(
            f"Seed research complete. {len(all_seeds)} seeds saved to data/seeds.json")
    else:
        print("No seeds found.")

    # Save technology counts
    with open('data/technology_counts.json', 'w') as f:
        json.dump(technology_counts, f, indent=4)

    return all_seeds


if __name__ == "__main__":
    seeds = run_seed_research()
    print(f"Generated {len(seeds)} seeds.")
    print("First 5 seeds:")
    for seed in seeds[:5]:
        print(f"- {seed}")
