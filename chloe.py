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
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)
console = Console()

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
        {"role": "system", "content": "You are Chloe, a terminal agent. Use your tools to manage files. Be concise."}
    ]

    console.print(Panel("[bold cyan]Chloe (Groq Edition) Active[/bold cyan]", expand=False))

    while True:
        user_input = console.input("[bold blue]>>> [/bold blue]")
        if user_input.lower() in ["exit", "quit"]:
            break

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=tools
        )

        response_message = response.choices[0].message

        if response_message.tool_calls:
            messages.append(response_message)
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                if function_name == "list_files":
                    result = list_files(**args)
                elif function_name == "search_files":
                    result = search_files(**args)
                elif function_name == "write_file":
                    result = write_file(**args)

                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": result,
                })

            second_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages
            )
            final_text = second_response.choices[0].message.content
            console.print(Markdown(final_text))
            messages.append({"role": "assistant", "content": final_text})
        else:
            final_text = response_message.content
            console.print(Markdown(final_text))
            messages.append({"role": "assistant", "content": final_text})

if __name__ == "__main__":
    chloe_chat()