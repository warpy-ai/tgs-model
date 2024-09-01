from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
import json

# Initialize the model
model = ChatAnthropic(model_name="claude-3-sonnet-20240229")

# Create prompt
command_generation_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in Bash scripting and Linux command-line operations."),
    ("human", """Given the following task description: "{description}", generate the appropriate Bash command that accomplishes this task.
    Ensure the command is syntactically correct and commonly used in Linux environments.
    Provide only the command itself, without any explanation.""")
])

# Create chain
command_generation_chain = LLMChain(
    llm=model,
    prompt=command_generation_prompt,
    output_parser=StrOutputParser()
)


class CommandGenerationAgent:
    def run(self, state):
        task_descriptions = state.get('task_descriptions', {})
        task_command_pairs = {}

        for idx, item in task_descriptions.items():
            description = item["description"]
            print(f"Generating command for task: {description}")

            bash_command = command_generation_chain.invoke(
                {"description": description})

            if bash_command:
                task_command_pairs[idx] = {
                    "invocation": description,
                    "cmd": bash_command.strip()
                }

        # Update state
        state['commands'] = task_command_pairs

        # Save to file
        with open('data/nl2bash_data.json', 'w') as f:
            json.dump(task_command_pairs, f, indent=4)

        print("Bash commands generated and saved to data/nl2bash_data.json")
        return state


if __name__ == "__main__":
    # For testing purposes
    agent = CommandGenerationAgent()
    initial_state = {
        'task_descriptions': {
            "1": {"description": "List all files in the current directory"},
            "2": {"description": "Check the disk usage of the current directory"}
        }
    }
    final_state = agent.run(initial_state)
    print(f"Generated commands: {final_state['commands']}")
