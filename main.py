from agents.orchestration import orchestrate
import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)


if __name__ == "__main__":
    print("Python path:")
    for path in sys.path:
        print(path)

    final_state = orchestrate()
    print(f"Final commands: {final_state['commands']}")
