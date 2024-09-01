from agents.seed_research_agent import run_seed_research
from agents.task_description_agent import run_task_description_generation
from agents.command_generation_agent import run_command_generation
from graph.graph_manager import initialize_graph, update_graph_with_command, run_graph, create_initial_state
import json


def orchestrate():
    run_seed_research()
    run_task_description_generation()
    run_command_generation()

    graph = initialize_graph()
    initial_state = create_initial_state()

    with open('data/nl2bash_data.json', 'r') as f:
        task_command_pairs = json.load(f)

    for idx, item in task_command_pairs.items():
        update_graph_with_command(graph, item['invocation'], item['cmd'])

    final_state = run_graph(initial_state)

    print("Orchestration complete. Data and graph updated successfully.")
    return final_state
