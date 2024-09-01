from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.tools import Tool
import json

# Prompt template for seed research
seed_research_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in Bash scripting and Linux systems administration."),
    ("human", """Identify common categories or tasks in Bash scripting. 
    These should be areas where Bash commands are frequently used, such as file operations, network management, system monitoring, etc.
    List at least 10 different categories.
    
    Provide your response as a comma-separated list.""")
])

# Initialize the Anthropic model
model = ChatAnthropic(model="claude-3-sonnet-20240229")

# Create the chain
seed_research_chain = seed_research_prompt | model | CommaSeparatedListOutputParser()

# Create a tool for the agent
seed_research_tool = Tool(
    name="SeedResearch",
    func=seed_research_chain.invoke,
    description="Use this tool to generate a list of common Bash scripting categories."
)

# Create the agent
agent_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI assistant tasked with researching Bash scripting categories."),
    ("human", "{input}"),
    ("human", "Use the SeedResearch tool to generate a list of common Bash scripting categories."),
    ("human", "Agent scratchpad: {agent_scratchpad}")
])

seed_research_agent = create_openai_tools_agent(
    llm=model,
    tools=[seed_research_tool],
    prompt=agent_prompt
)

# Create the agent executor
agent_executor = AgentExecutor(
    agent=seed_research_agent, tools=[seed_research_tool])


class SeedResearchAgent:
    def run(self, state):
        # Run the agent to get a list of seed topics
        result = agent_executor.invoke(
            {"input": "Generate a list of Bash scripting categories"})

        # Extract the seed list from the result
        seed_list = result.get('output', [])

        # Update the state with the new seeds
        state['seeds'] = seed_list

        # Save the seeds to a file for later use
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
