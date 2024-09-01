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
    ("system", "You are an expert in describing Bash scripting tasks. Provide a concise task instruction similar to those found in system administration or DevOps documentation."),
    ("human", """Generate a concise task instruction for a Bash scripting task related to: {seed}

Your response should be a single sentence that clearly describes the task to be performed, similar to the following examples:
- Display the current CPU usage for all processes.
- List the top 10 memory-consuming processes.
- Monitor real-time CPU load every 2 seconds.
- Show disk read and write statistics.

Task instruction:""")
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

        print("Task instructions generated and saved.")
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
