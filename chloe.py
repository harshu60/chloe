import os
import json
import fnmatch
from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

load_dotenv()

client = OpenAI(
    api_key=os.getenv("AI_API_KEY"),
    base_url=os.getenv("AI_BASE_URL")
)
model = os.getenv("AI_MODEL", "mimo-v2.6-flash")
console = Console()

def read_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Failed to read file: {e}"
    
def list_files(directory="."):
    try:
        files = os.listdir(directory)
        return "\n".join(files)
    except Exception as e:
        return f"Error listing files: {e}"

def search_files(query, path="."):
    matches = []
    try:
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, f"*{query}*"):
                matches.append(os.path.join(root, filename))
        return "\n".join(matches) if matches else "No files found."
    except Exception as e:
        return f"Search error: {e}"

def write_file(filename, content):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to {filename}"
    except Exception as e:
        return f"Failed to write file: {e}"

tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read and return the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Path to the file to read"
                    }
                },
                "required": ["filename"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files in a directory",
            "parameters": {
                "type": "object",
                "properties": {"directory": {"type": "string"}},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_files",
            "description": "Search for files by name in the current path",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Create or overwrite a file with content",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["filename", "content"],
            },
        },
    },
]

def chloe_chat():
    messages = [
        {
            "role": "system",
            "content": (
                "You are Chloe, a terminal agent. Use tools when needed. "
                "After using a tool, explain the result briefly."
            ),
        }
    ]

    console.print(
        Panel(f"[bold cyan]Chloe ({model}) Active[/bold cyan]", expand=False)
    )

    while True:
        user_input = console.input("[bold blue]>>> [/bold blue]")

        if user_input.lower().strip() in {"exit", "quit"}:
            break

        messages.append({"role": "user", "content": user_input})

        while True:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice="auto",
            )

            response_message = response.choices[0].message

            if not response_message.tool_calls:
                final_text = response_message.content or ""
                console.print(Markdown(final_text))
                messages.append(
                    {"role": "assistant", "content": final_text}
                )
                break

            assistant_message = {
                "role": "assistant",
                "content": response_message.content or "",
                "tool_calls": [
                    {
                        "id": call.id,
                        "type": "function",
                        "function": {
                            "name": call.function.name,
                            "arguments": call.function.arguments,
                        },
                    }
                    for call in response_message.tool_calls
                ],
            }
            messages.append(assistant_message)

            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name

                try:
                    args = json.loads(tool_call.function.arguments)

                    if function_name == "read_file":
                        result = read_file(**args)
                    elif function_name == "list_files":
                        result = list_files(**args)
                    elif function_name == "search_files":
                        result = search_files(**args)
                    elif function_name == "write_file":
                        result = write_file(**args)
                    else:
                        result = f"Unknown tool: {function_name}"

                except Exception as error:
                    result = f"Tool error: {error}"

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result),
                    }
                )


if __name__ == "__main__":
    chloe_chat()