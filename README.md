# Agent Frameworks – Side-by-Side Examples

The **same small AI agent** built with four different agent frameworks, so you can compare them.
Ask it *"What time is it in Tokyo?"* and it tells you the current time there.

| File | Framework | Company | Model it uses |
|---|---|---|---|
| `google_adk_agent/` | Google ADK | Google | Gemini, OpenAI or Azure (your choice) |
| `openai_adk_agent.py` | OpenAI Agents SDK | OpenAI | GPT |
| `aws_adk_agent.py` | Strands Agents | AWS | Claude on Amazon Bedrock |
| `azure_adk_agent.py` | Microsoft Agent Framework | Microsoft | Azure OpenAI |

## The idea behind every agent framework

Every framework has the same three parts. Only the names change:

1. **Tool**: a normal Python function the AI is allowed to call (here: `get_current_time`).
2. **Agent**: a **model** + **instructions** + **tools**.
3. **Runner**: sends your question to the agent, runs the tools the model asks for,
   and gives back the final answer. It also remembers the chat.

```
You ──► Runner ──► Agent (model + instructions)
                     │  "I need the time in Tokyo"
                     ▼
                   Tool: get_current_time("Tokyo", "Asia/Tokyo")
                     │  returns "09:30 PM"
                     ▼
You ◄── Runner ◄── "It's 9:30 PM in Tokyo."
```

| | Google ADK | OpenAI Agents SDK | AWS Strands | Microsoft Agent Framework |
|---|---|---|---|---|
| Make a tool | plain function | `@function_tool` | `@tool` | `@tool` |
| Make the agent | `Agent(model, instruction, tools)` | `Agent(model, instructions, tools)` | `Agent(model, system_prompt, tools)` | `Agent(client, instructions, tools)` |
| Ask a question | `adk web` / `adk run` (built in) | `Runner.run_sync(agent, ...)` | `agent("question")` | `await agent.run("question")` |
| Remember the chat | built in (session) | pass `history` back in | built in | `session` |

## 1. Install

With [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

Or with pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Add your keys

```bash
cp .env.example .env
```

Open `.env` and fill in the keys for the framework you want to try.
You only need keys for the ones you run.

## 3. Run

**Google ADK** (choose the model with `MODEL_PROVIDER` in `.env`):

```bash
uv run adk web                    # chat page at http://127.0.0.1:8000
uv run adk run google_adk_agent   # chat in the terminal
```

**OpenAI Agents SDK:**

```bash
uv run python openai_adk_agent.py
```

**AWS Strands Agents:**

```bash
uv run python aws_adk_agent.py
```

**Microsoft Agent Framework (Azure):**

```bash
uv run python azure_adk_agent.py
```

Type `exit` to stop. Using pip? Drop `uv run` from the commands.

## Project files

```
google_adk_agent/        # Google ADK
  __init__.py            #   picks the model with MODEL_PROVIDER
  gemini_agent.py        #   Google ADK + Gemini
  openai_agent.py        #   Google ADK + OpenAI
  azure_agent.py         #   Google ADK + Azure OpenAI
openai_adk_agent.py      # OpenAI Agents SDK
aws_adk_agent.py         # AWS Strands Agents
azure_adk_agent.py       # Microsoft Agent Framework
.env.example             # sample keys – copy to .env
```
