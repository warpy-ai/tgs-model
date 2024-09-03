import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
from logs.generation_logs import logger

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found in .env file")

# Initialize the model
model = ChatAnthropic(model_name="claude-3-sonnet-20240229",
                      anthropic_api_key=ANTHROPIC_API_KEY)

# Create prompt
task_description_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in Bash scripting, system administration, and DevOps practices."),
    ("human", """Generate a specific and practical Bash scripting task related to: {seed}

Your response should be a single sentence that clearly describes a task to be performed using Bash, similar to the following examples:
- Create a Bash script to monitor CPU usage and send an alert if it exceeds 90% for more than 5 minutes.
- Implement a Bash function to recursively search for and delete files older than 30 days in a specified directory.
- Write a Bash script to automate the process of creating a new Git branch, committing changes, and pushing to a remote repository.

Task description:""")
])

# Create chain
task_description_chain = task_description_prompt | model | StrOutputParser()


class TaskDescriptionAgent:
    def run(self, state):
        seeds = state.get('seeds', [])
        task_descriptions = {}
        task_command_pairs = {}

        for idx, seed in enumerate(seeds):
            # Generate task instruction
            task_instruction = task_description_chain.invoke({"seed": seed})
            if task_instruction:
                # Remove any leading/trailing whitespace and ensure it ends with a period
                task_instruction = task_instruction.strip().rstrip('.') + '.'

                task_descriptions[str(
                    idx + 1)] = {"seed": seed, "description": task_instruction}
                task_command_pairs[str(idx + 1)] = {
                    "invocation": task_instruction,
                    "cmd": ""  # This will be filled by the command generation agent
                }

                logger.log_task_description(
                    seed, task_instruction, task_instruction)

        # Update state
        state['task_descriptions'] = task_descriptions
        state['commands'] = task_command_pairs

        # Save to files
        os.makedirs('data', exist_ok=True)
        with open('data/task_descriptions.json', 'w') as f:
            json.dump(task_descriptions, f, indent=4)

        with open('data/nl2bash_data.json', 'w') as f:
            json.dump(task_command_pairs, f, indent=4)

        print(
            f"Generated {len(task_descriptions)} task descriptions and saved them to data/task_descriptions.json and data/nl2bash_data.json")
        return state


def run_task_description_generation():
    agent = TaskDescriptionAgent()
    with open('data/seeds.json', 'r') as f:
        seeds = json.load(f)
    initial_state = {'seeds': seeds}
    final_state = agent.run(initial_state)
    return final_state['task_descriptions']


if __name__ == "__main__":
    task_descriptions = run_task_description_generation()
    print(f"Generated task descriptions: {task_descriptions}")
