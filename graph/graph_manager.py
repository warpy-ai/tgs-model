from typing import TypedDict, List
from langchain_core.messages import BaseMessage
from logs.generation_logs import logger
from langgraph.graph import StateGraph, END

# Define the state schema


class AgentState(TypedDict):
    messages: List[BaseMessage]
    seeds: List[str]
    task_descriptions: dict
    commands: dict


def initialize_graph():
    # Create the graph
    workflow = StateGraph(AgentState)

    # Add a single node for processing commands
    workflow.add_node("process_command", process_command)

    # Set the entry point
    workflow.set_entry_point("process_command")

    # Add an edge from the process node to END
    workflow.add_edge("process_command", END)

    # Compile the graph
    return workflow.compile()


def process_command(state: AgentState) -> AgentState:
    # Process each command in the state
    for invocation, cmd in state['commands'].items():
        logger.log_graph_update(invocation, cmd)
        # Here you can add any additional processing logic
        print(f"Processed command: {invocation} - {cmd}")
    return state


def update_graph_with_command(state: AgentState, invocation: str, cmd: str) -> AgentState:
    # Update the state with the new command
    if 'commands' not in state:
        state['commands'] = {}
    state['commands'][invocation] = cmd
    logger.log_graph_update(invocation, cmd)
    return state


def run_graph(initial_state: AgentState):
    graph = initialize_graph()
    final_state = graph.invoke(initial_state)
    return final_state

# Helper function to create initial state


def create_initial_state() -> AgentState:
    return AgentState(
        messages=[],
        seeds=[],
        task_descriptions={},
        commands={}
    )


if __name__ == "__main__":
    # For testing purposes
    initial_state = create_initial_state()
    initial_state = update_graph_with_command(
        initial_state, "List files", "ls -la")
    initial_state = update_graph_with_command(
        initial_state, "Check disk usage", "du -h")
    final_state = run_graph(initial_state)
    print("Final state:")
    print(f"Commands: {final_state['commands']}")
