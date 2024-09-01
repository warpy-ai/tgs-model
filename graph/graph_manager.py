from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
import operator
from logs.generation_logs import logger

# Define the state schema


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    seeds: list[str]
    task_descriptions: dict
    commands: dict


def initialize_graph():
    # Create the graph
    workflow = StateGraph(AgentState)

    # Add a single node for updating the graph
    workflow.add_node("update_graph", update_graph_node)

    # Set the entry point
    workflow.set_entry_point("update_graph")

    # Add an edge from the update node to END
    workflow.add_edge("update_graph", END)

    # Compile the graph
    return workflow.compile()


def update_graph_node(state: AgentState) -> AgentState:
    # This node doesn't need to do anything as the graph is already updated
    # We're just using it as a placeholder in the LangGraph structure
    return state


def update_graph_with_command(graph, invocation, cmd):
    # Implement the logic to update the graph with the new command
    logger.log_graph_update(invocation, cmd)
    # In this implementation, we're not actually updating the graph structure
    # Instead, we're updating the state that will be passed through the graph
    current_state = graph.get_current_state()
    if 'commands' not in current_state:
        current_state['commands'] = {}
    current_state['commands'][invocation] = cmd
    graph.set_current_state(current_state)


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
    graph = initialize_graph()
    update_graph_with_command(graph, "List files", "ls -la")
    update_graph_with_command(graph, "Check disk usage", "du -h")
    final_state = run_graph(initial_state)
    print("Final state:")
    print(f"Commands: {final_state['commands']}")
