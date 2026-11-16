# 🤖 Chloe — Terminal AI Assistant & Agent

Chloe is a lightweight, terminal-based AI assistant built in Python. It runs as an interactive CLI agent that connects an LLM to a small set of local tools, so it can read, list, search, and write files while chatting with you.

---

## 📌 Overview

Chloe goes beyond a plain chat interface by acting as an operational terminal agent:

* **Tool Calling & Execution:** Sends tool definitions to the model and executes the returned function calls locally, feeding results back into the conversation.
* **Terminal UX:** Styled with the `rich` library — panels, markdown rendering, and formatted code blocks.
* **OpenAI-Compatible Endpoints:** Works with any OpenAI-style API (Groq, DeepSeek, local servers, etc.) via a configurable base URL.

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Agent loop and tool definitions |
| **LLM Provider** | Any OpenAI-compatible API | Text generation and tool-call reasoning |
| **Terminal UI** | `rich` | Rich-text rendering and markdown displays |
| **Config** | `python-dotenv` | Loads API credentials from `.env` |

---

## 🚀 Key Features

* **File Operations:** Reads, lists, searches, and writes files directly from the prompt.
* **Multi-Turn Tool Loop:** Keeps calling tools until the model produces a final answer, then renders it as markdown.
* **Resilient Execution:** Tool arguments and API responses are wrapped in error handling so a malformed call doesn't crash the session.
* **Minimal Setup:** Single-file implementation with three dependencies.

---

## 📂 Project Structure

```text
chloe/
├── chloe.py           # Agent loop, tool definitions, and CLI entry point
├── requirements.txt   # Project library dependencies
├── .env               # API credentials (not committed)
└── README.md          # This file
```

---

## ⚙️ Setup

**1. Install dependencies**

```bash
pip install -r requirements.txt
```

**2. Create a `.env` file**

```env
AI_API_KEY=your-api-key-here
AI_BASE_URL=https://your-api-endpoint.example/v1
AI_MODEL=your-model-name
```

| Variable | Required | Description |
| :--- | :--- | :--- |
| `AI_API_KEY` | Yes | API key sent to the provider |
| `AI_BASE_URL` | Yes | Base URL of an OpenAI-compatible endpoint |
| `AI_MODEL` | No | Model name — defaults to `mimo-v2.6-flash` |

---

## ▶️ Usage

```bash
python chloe.py
```

Type your message at the `>>>` prompt. Enter `exit` or `quit` to leave.

```text
Chloe (mimo-v2.6-flash) Active
>>> list the files in this directory
```
