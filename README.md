# 🤖 Chloe — Terminal AI Assistant & Agent

Chloe is a lightweight, terminal-based AI assistant built in Python. Designed as an interactive CLI agent, Chloe leverages fast LLM inference alongside native system tools to handle conversations, file operations, and terminal workflows.

---

## 📌 Overview

Chloe functions beyond a standard chat interface by acting as an operational terminal agent:
* **Tool Calling & Execution:** Connects LLM reasoning directly to executable functions for file exploration and local operations.
* **Terminal UX:** Styled using the `rich` library to deliver formatted outputs, syntax-highlighted code blocks, and clear status states.
* **Low Latency:** Uses high-throughput API endpoints (Groq / DeepSeek) to deliver near-instant conversational and functional responses.

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Core agent loops and tool definitions |
| **LLM Provider** | Groq / DeepSeek API | High-speed text generation and structured reasoning |
| **Terminal UI** | `rich` | Rich-text rendering, markdown displays, and tables |
| **Environment** | Linux / Windows | POSIX shell script runner and cross-platform support |

---

## 🚀 Key Features

* **File Operations & Management:** Inspects directories, reads files, and assists with desktop file handling directly via prompt commands.
* **Structured System Prompting:** Configured with a dedicated assistant persona to keep responses focused, concise, and technically grounded.
* **Resilient Execution:** Safely parses API responses and tool call arguments to prevent unhandled script crashes during execution.

---

## 📂 Project Structure

```text
chloe/
├── agent/            # Core conversational loop & system prompts
├── tools/            # File management & local execution utilities
├── main.py           # CLI entry point & user input loop
├── start.sh          # Quick launch script for Linux environments
├── requirements.txt  # Project library dependencies
└── .env.example      # API key environment varia
ble template
