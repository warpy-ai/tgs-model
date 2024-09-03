from agents.seed_research_agent import run_seed_research
from agents.command_generation_agent import run_command_generation
from graph.graph_manager import initialize_graph, update_graph_with_command, run_graph, create_initial_state
from logs.generation_logs import logger
import json


def orchestrate():
    commands = run_command_generation()

    initial_state = create_initial_state()

    for idx, command in commands.items():
        initial_state = update_graph_with_command(
            initial_state, command['invocation'], command['cmd'])

    final_state = run_graph(initial_state)

    logger.log('orchestration_complete', {
        'num_commands': len(commands),
        # Convert to string to ensure it's JSON serializable
        'final_state': str(final_state)
    })

    print("Orchestration complete. Data and graph updated successfully.")

    # Save the final state to a file
    with open('data/final_state.json', 'w') as f:
        json.dump({
            'commands': commands
        }, f, indent=4)

    return final_state


if __name__ == "__main__":
    final_state = orchestrate()
    print(f"Final commands: {final_state['commands']}")
