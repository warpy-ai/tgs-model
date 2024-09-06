import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
from logs.generation_logs import logger
from utils.rate_limiter import RateLimiter

# Load environment variables from .env file
load_dotenv()
rate_limiter = RateLimiter(requests_per_minute=50, tokens_per_minute=40000)

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
    ("human", """Given the following task description: "{description}", generate the appropriate Bash command or script that accomplishes this task.
    Ensure the command is syntactically correct and commonly used in Linux environments.
    If a single command is not sufficient, provide a short Bash script.
    It must be a one line command.
    Provide only the command or script itself, without any explanation.""")
])

# Create chain
command_generation_chain = command_generation_prompt | model | StrOutputParser()


def load_existing_commands():
    if os.path.exists('data/commands.json'):
        with open('data/commands.json', 'r') as f:
            return json.load(f)
    return {}


def save_commands_to_file(commands):
    with open('data/commands.json', 'w') as f:
        json.dump(commands, f, indent=4)


class CommandGenerationAgent:
    def run(self):
        # Load seeds from seeds.json
        with open('data/seeds.json', 'r') as f:
            seeds = json.load(f)

        existing_commands = load_existing_commands()
        next_index = str(max(
            int(key) for key in existing_commands.keys()) + 1) if existing_commands else "1"

        for idx, description in enumerate(seeds):
            # Check if the description already exists
            if any(cmd['invocation'] == description for cmd in existing_commands.values()):
                print(
                    f"Skipping already existing command for task: {description}")
                continue

            print(f"Generating command for task: {description}")
            estimated_tokens_for_request = 1000  # Example estimation
            rate_limiter.wait(tokens=estimated_tokens_for_request)

            bash_command = command_generation_chain.invoke(
                {"description": description})

            print(f"Generated command: {bash_command}")
            if bash_command:
                existing_commands[next_index] = {
                    "invocation": description,
                    "cmd": bash_command.strip()
                }
                logger.log_command(description, bash_command.strip())

                # Save immediately after appending
                save_commands_to_file(existing_commands)

                # Increment the index for the next command
                next_index = str(int(next_index) + 1)

        print("Bash commands generated and saved to data/commands.json")
        return existing_commands


def run_command_generation():
    print("Running command generation agent...")
    agent = CommandGenerationAgent()
    return agent.run()


if __name__ == "__main__":
    commands = run_command_generation()
    print(f"Generated commands: {commands}")
