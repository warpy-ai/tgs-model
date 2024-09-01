from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
import json

# Initialize the model
model = ChatAnthropic(model_name="claude-3-sonnet-20240229")

# Create prompts
task_description_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in describing Bash scripting tasks."),
    ("human",
     "Generate a natural language description for a task related to: {seed}")
])

bash_command_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in Bash scripting."),
    ("human",
     "Generate a Bash command for the following task: {task_description}")
])

# Create chains
task_description_chain = LLMChain(
    llm=model,
    prompt=task_description_prompt,
    output_parser=StrOutputParser()
)

bash_command_chain = LLMChain(
    llm=model,
    prompt=bash_command_prompt,
    output_parser=StrOutputParser()
)


class TaskDescriptionAgent:
    def run(self, state):
        seeds = state.get('seeds', [])
        task_descriptions = {}
        task_command_pairs = {}

        for idx, seed in enumerate(seeds):
            # Generate task description
            description = task_description_chain.invoke({"seed": seed})
            if description:
                task_descriptions[str(
                    idx + 1)] = {"seed": seed, "description": description}

                # Generate Bash command
                command = bash_command_chain.invoke(
                    {"task_description": description})
                if command:
                    task_command_pairs[str(idx + 1)] = {
                        "invocation": description,
                        "cmd": command
                    }

        # Update state
        state['task_descriptions'] = task_descriptions
        state['commands'] = task_command_pairs

        # Save to files
        with open('data/task_descriptions.json', 'w') as f:
            json.dump(task_descriptions, f, indent=4)

        with open('data/nl2bash_data.json', 'w') as f:
            json.dump(task_command_pairs, f, indent=4)

        print("Task descriptions and commands generated and saved.")
        return state


if __name__ == "__main__":
    # For testing purposes
    agent = TaskDescriptionAgent()
    initial_state = {'seeds': ["File operations",
                               "Network management", "System monitoring"]}
    final_state = agent.run(initial_state)
    print(f"Generated task descriptions: {final_state['task_descriptions']}")
    print(f"Generated commands: {final_state['commands']}")
