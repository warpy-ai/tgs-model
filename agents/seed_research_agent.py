import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser
import json
from logs.generation_logs import logger
from utils.rate_limiter import rate_limiter
import time
from anthropic import InternalServerError

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found in .env file")

# Initialize the model with rate limiting


class RateLimitedChatAnthropic(ChatAnthropic):
    def generate(self, messages, stop=None, **kwargs):
        max_retries = 3
        retry_delay = 5  # seconds

        for attempt in range(max_retries):
            try:
                # Estimate token usage
                estimated_tokens = sum(len(str(m).split())
                                       for m in messages) * 1.3
                rate_limiter.wait(int(estimated_tokens))
                return super().generate(messages, stop=stop, **kwargs)
            except InternalServerError as e:
                if attempt < max_retries - 1:
                    print(
                        f"Encountered an Internal Server Error. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    raise e

        raise Exception("Max retries reached. Unable to complete the request.")


model = RateLimitedChatAnthropic(
    model_name="claude-3-sonnet-20240229", anthropic_api_key=ANTHROPIC_API_KEY)

# Prompt template for seed research
seed_research_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in Bash scripting and Linux systems administration."),
    ("human", """Identify common categories or tasks in Bash scripting. 
    These should be areas where Bash commands are frequently used, such as file operations, network management, system monitoring, etc.
    List at least 10 different categories.
    
    Provide your response as a comma-separated list.""")
])

# Create the chain
seed_research_chain = seed_research_prompt | model | CommaSeparatedListOutputParser()


class SeedResearchAgent:
    def run(self, state):
        # Run the chain to get a list of seed topics
        seed_list = seed_research_chain.invoke({})

        # Update the state with the new seeds
        state['seeds'] = seed_list

        for seed in seed_list:
            logger.log_seed(seed)

        # Save the seeds to a file for later use
        os.makedirs('data', exist_ok=True)
        with open('data/seeds.json', 'w') as f:
            json.dump(seed_list, f, indent=4)

        print("Seed research complete. Seeds saved to data/seeds.json")
        return state


def run_seed_research():
    agent = SeedResearchAgent()
    initial_state = {'seeds': []}
    final_state = agent.run(initial_state)
    return final_state['seeds']


if __name__ == "__main__":
    seeds = run_seed_research()
    print(f"Generated seeds: {seeds}")
