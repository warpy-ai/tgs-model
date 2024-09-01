from agents.seed_research_agent import run_seed_research
from agents.task_description_agent import run_task_description_generation
from agents.command_generation_agent import run_command_generation
from graph.graph_manager import initialize_graph, update_graph_with_command, run_graph, create_initial_state
import json
from logs.generation_logs import logger


def orchestrate():
    seeds = run_seed_research()
    task_descriptions = run_task_description_generation()
    commands = run_command_generation()

    graph = initialize_graph()
    initial_state = create_initial_state()

    for idx, command in commands.items():
        update_graph_with_command(graph, command['invocation'], command['cmd'])

    final_state = run_graph(initial_state)

    logger.log('orchestration_complete', {
        'num_seeds': len(seeds),
        'num_task_descriptions': len(task_descriptions),
        'num_commands': len(commands),
        'final_state': final_state
    })

    print("Orchestration complete. Data and graph updated successfully.")
    return final_state


if __name__ == "__main__":
    final_state = orchestrate()
    print(f"Final commands: {final_state['commands']}")
