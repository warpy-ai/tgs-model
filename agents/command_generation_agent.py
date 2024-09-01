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
command_generation_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in Bash scripting and Linux command-line operations."),
    ("human", """Given the following task description: "{description}", generate the appropriate Bash command that accomplishes this task.
    Ensure the command is syntactically correct and commonly used in Linux environments.
    Provide only the command itself, without any explanation.""")
])

# Create chain
command_generation_chain = command_generation_prompt | model | StrOutputParser()


class CommandGenerationAgent:
    def run(self, state):
        task_descriptions = state.get('task_descriptions', {})
        commands = {}

        for idx, item in task_descriptions.items():
            description = item["description"]
            print(f"Generating command for task: {description}")

            bash_command = command_generation_chain.invoke(
                {"description": description})

            if bash_command:
                commands[idx] = {
                    "invocation": description,
                    "cmd": bash_command.strip()
                }
                logger.log_command(description, bash_command.strip())

        # Update state
        state['commands'] = commands

        # Save to file
        with open('data/commands.json', 'w') as f:
            json.dump(commands, f, indent=4)

        print("Bash commands generated and saved to data/nl2bash_data.json")
        return state


def run_command_generation():
    agent = CommandGenerationAgent()
    try:
        with open('data/task_descriptions.json', 'r') as f:
            task_descriptions = json.load(f)
    except FileNotFoundError:
        print(
            "Warning: data/task_descriptions.json not found. Using empty task descriptions.")
        task_descriptions = {}

    initial_state = {'task_descriptions': task_descriptions}
    final_state = agent.run(initial_state)
    return final_state['commands']


if __name__ == "__main__":
    commands = run_command_generation()
    print(f"Generated commands: {commands}")
