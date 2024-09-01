from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()

env_api_key = os.getenv("OPEN_AI")

client = OpenAI(
    api_key=env_api_key,
)

# Load the finetune.txt file

with open("data/finetune.txt", "r") as f:
    lines = f.readlines()


# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API


def run_conversation(line):
    # Step 1: send the conversation and available functions to the model
    messages = [
        {"role": "user", "content":
         "Generate a bash command base on this task description: " + str(line)}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_bash_command",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "cmd": {"type": "string", "description": "The bash command to run"},
                    },
                    "required": ["location"],
                },
            },
        }
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )

    response_message = response.choices[0].message.tool_calls

    print("Processed message")

    if response_message is None:
        print("No response")
        return

    cmd = json.loads(response_message[0].function.arguments)["cmd"]

    newObject = json.dumps({"invocation": line, "cmd": cmd})
    print("Finished")
    return newObject


task_command_object = {}

for indx, line in enumerate(lines):
    print("started line " + str(indx + 1))
    commands = run_conversation(line)
    if commands is not None:
        task_command_object[str(indx + 1)] = commands


with open("data/new-nl2bash-data.json", "w") as f:
    json.dump(task_command_object, f, indent=4)


print("Finished")
