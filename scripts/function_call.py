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
    lines = f.read()


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

    print(response)
    response_message = response.choices[0].message

    return response_message


# print(run_conversation())

for line in lines[:1]:
    print("this is line " + line)
    run_conversation(line)
