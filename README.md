# AI Agents – One Agent, Four Frameworks

Learn how AI agents work by building **the same small agent** with four popular agent frameworks:

| Framework | Made by | Code in this repo |
|---|---|---|
| Google ADK (Agent Development Kit) | Google | [`google_adk_agent/`](google_adk_agent/) |
| OpenAI Agents SDK | OpenAI | [`openai_adk_agent.py`](openai_adk_agent.py) |
| Strands Agents | AWS (Amazon) | [`aws_adk_agent.py`](aws_adk_agent.py) |
| Microsoft Agent Framework | Microsoft (Azure) | [`azure_adk_agent.py`](azure_adk_agent.py) |

**The agent:** you ask *"What time is it in Tokyo?"* and it tells you the real current time there.

---

## Contents

1. [What is an AI agent?](#1-what-is-an-ai-agent)
2. [What is an agent framework (ADK)?](#2-what-is-an-agent-framework-adk)
3. [The core concepts](#3-the-core-concepts)
4. [How one question flows through an agent](#4-how-one-question-flows-through-an-agent)
5. [The same agent in four frameworks](#5-the-same-agent-in-four-frameworks)
6. [Setup and run](#6-setup-and-run)
7. [Project files](#7-project-files)
8. [Glossary](#8-glossary)
9. [Practice exercises](#9-practice-exercises)
10. [Common problems](#10-common-problems)

---

## 1. What is an AI agent?

A normal chatbot can only **talk**. It answers from what it learned during training.

An **AI agent** can also **do things**. It can call functions, look things up, and use the
results to give a better answer.

> **Example:** Ask a plain chatbot *"What time is it in Tokyo?"* It doesn't know the
> current time, so it may guess or give a wrong answer.
> An agent instead **calls a function** that reads the real clock, then answers with the correct time.

**Simple way to remember it:**

```
Chatbot = brain
Agent   = brain + hands (tools) + a plan for when to use them
```

---

## 2. What is an agent framework (ADK)?

An **agent framework** (Google calls theirs an **ADK – Agent Development Kit**) is a Python library
that does the boring work of building an agent for you:

- sends your question to the AI model
- tells the model which tools it can use
- runs the tool when the model asks for it
- sends the tool's result back to the model
- remembers the conversation
- gives you the final answer

Without a framework you would write all of that yourself. With a framework, you write a few lines.

> **Analogy:** The AI model is a **chef**. Tools are the **kitchen equipment**. The framework is
> the **restaurant manager**: it takes the order, hands the chef the right equipment,
> and brings the finished dish back to the customer.

---

## 3. The core concepts

Every framework in this repo is built from the same building blocks. Only the names change.

### 3.1 Model (the brain)

The **model** is the AI that reads, thinks and writes. Examples: Gemini (Google), GPT (OpenAI),
Claude (Anthropic, available on AWS Bedrock).

```python
model="gemini-4-argon"        # Google ADK
model="gpt-6-astra"           # OpenAI Agents SDK
```

### 3.2 Instructions (the job description)

**Instructions** (also called a *system prompt*) tell the model **who it is** and **how to behave**.
The user doesn't see them, but the model follows them on every message.

```python
instruction="You tell the current time in cities. Always use the get_current_time tool. Never guess."
```

### 3.3 Tool (the hands)

A **tool** is a **normal Python function** that the model is allowed to call.
The model reads the function's **name**, **parameters** and **docstring** to understand
what it does and when to use it, so a clear docstring matters.

```python
def get_current_time(city: str, timezone: str) -> dict:
    """Returns the current time in a specified city."""
    ...
```

> **Important:** the model does **not** run the code itself. It only *asks* for the tool to be run
> (for example: "call get_current_time with city=Tokyo, timezone=Asia/Tokyo").
> The **framework** runs the function and hands the result back to the model.

### 3.4 Agent (the worker)

An **agent** puts it all together:

```
Agent = Model + Instructions + Tools
```

```python
agent = Agent(model=..., instruction=..., tools=[get_current_time])
```

### 3.5 Runner (the loop that makes it work)

The **runner** is what actually runs the agent. It sends the question, runs the tools the model
asks for, sends results back, and repeats until the model gives a final answer.
This repeat-until-done cycle is called the **agent loop**.

### 3.6 Session / Memory (remembering the chat)

A **session** stores the conversation so far, so the agent understands follow-up questions.

> **Example:**
> You: *"What time is it in Paris?"* → Agent: *"3:00 PM"*
> You: *"And in London?"* → the agent knows you're still asking about the **time**, because of the session.

### 3.7 Environment variables (`.env`)

API keys are like passwords. We keep them in a file named **`.env`**, which is **never uploaded to GitHub**.
The code reads them with `os.getenv("GOOGLE_API_KEY")`.
`.env.example` is a safe template with fake values that shows which keys you need.

---

## 4. How one question flows through an agent

```
 You: "What time is it in Tokyo?"
  │
  ▼
 RUNNER ── sends question + instructions + list of tools ──►  MODEL
                                                               │
                                     "I need a tool: call      │
                                      get_current_time(        │
                                      'Tokyo','Asia/Tokyo')"   │
  ┌────────────────────────────────────────────────────────────┘
  ▼
 RUNNER runs the Python function  ──►  TOOL returns {"time": "09:30 PM", ...}
  │
  ▼
 RUNNER ── sends the tool result back ──►  MODEL
                                            │
                     "It's 9:30 PM in Tokyo."│
  ┌─────────────────────────────────────────┘
  ▼
 You see: "It's 9:30 PM in Tokyo."
```

**In short:** question → model decides → tool runs → model reads the result → answer.

---

## 5. The same agent in four frameworks

### 5.1 Side-by-side comparison

| Concept | Google ADK | OpenAI Agents SDK | AWS Strands | Microsoft Agent Framework |
|---|---|---|---|---|
| Install | `google-adk` | `openai-agents` | `strands-agents` | `agent-framework-core` |
| Make a tool | plain function | `@function_tool` | `@tool` | `@tool` |
| Instructions are called | `instruction` | `instructions` | `system_prompt` | `instructions` |
| Make the agent | `Agent(model, instruction, tools)` | `Agent(model, instructions, tools)` | `Agent(model, system_prompt, tools)` | `Agent(client, instructions, tools)` |
| Run it | `adk web` / `adk run` (built in) | `Runner.run_sync(agent, ...)` | `agent("question")` | `await agent.run("question")` |
| Memory | built-in session | pass `history` back in | built in | `session` object |
| Works with models from | Gemini (built in) + many others via LiteLLM | OpenAI | Amazon Bedrock (and others) | Azure OpenAI / OpenAI (and others) |
| Extra goodies | web chat UI, sub-agents | handoffs between agents | AWS integration | Azure integration, workflows |

### 5.2 Google ADK – [`google_adk_agent/`](google_adk_agent/)

Google ADK expects a **folder** with a variable called **`root_agent`**. The `adk` command finds it
and gives you a chat page (`adk web`) or a terminal chat (`adk run`) for free.

```python
from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model="gemini-4-argon",
    name="root_agent",
    instruction="You tell the current time in cities...",
    tools=[get_current_time],          # a plain Python function
)
```

To use a **non-Google model**, wrap it in `LiteLlm`. Nothing else changes:

```python
from google.adk.models.lite_llm import LiteLlm

model=LiteLlm(model="openai/gpt-6-astra")      # OpenAI
model=LiteLlm(model="azure/gpt-4o-mini", ...)  # Azure OpenAI
```

That's why this folder has three files (`gemini_agent.py`, `openai_agent.py`, `azure_agent.py`).
`__init__.py` picks one based on `MODEL_PROVIDER` in `.env`.

### 5.3 OpenAI Agents SDK – [`openai_adk_agent.py`](openai_adk_agent.py)

```python
from agents import Agent, Runner, function_tool

@function_tool                                  # turns the function into a tool
def get_current_time(city: str, timezone: str) -> dict: ...

agent = Agent(name="time_agent", model="gpt-6-astra",
              instructions="...", tools=[get_current_time])

result = Runner.run_sync(agent, "What time is it in Tokyo?")
print(result.final_output)
```

Memory: we keep `result.to_input_list()` and send it back with the next question.

### 5.4 AWS Strands Agents – [`aws_adk_agent.py`](aws_adk_agent.py)

```python
from strands import Agent, tool
from strands.models import BedrockModel

@tool
def get_current_time(city: str, timezone: str) -> dict: ...

agent = Agent(model=BedrockModel(model_id="global.anthropic.claude-sonnet-4-6"),
              system_prompt="...", tools=[get_current_time])

print(agent("What time is it in Tokyo?"))       # just call the agent like a function
```

The simplest of the four: the agent **is** the runner, and it remembers the chat on its own.

### 5.5 Microsoft Agent Framework – [`azure_adk_agent.py`](azure_adk_agent.py)

Microsoft's new framework that replaces **Semantic Kernel** and **AutoGen**.

```python
from agent_framework import Agent, tool
from agent_framework.openai import OpenAIChatCompletionClient

@tool
def get_current_time(city: str, timezone: str) -> dict: ...

agent = Agent(client=OpenAIChatCompletionClient(azure_endpoint=..., api_key=..., model=...),
              instructions="...", tools=[get_current_time])

session = agent.create_session()                # memory
response = await agent.run("What time is it in Tokyo?", session=session)
print(response.text)
```

Here the model connection is called a **client**. It uses `async`/`await`, so it runs inside `asyncio.run(...)`.

### 5.6 What to notice

- **The tool function is identical in every file.** Only the decorator (`@tool`, `@function_tool`) changes.
- **The instructions are identical.** Only the parameter name changes.
- The frameworks mostly differ in **how you run the agent** and **how memory is kept**.
- Learn the concepts once, and you can pick up any framework quickly.

---

## 6. Setup and run

### Step 1: Install

With [uv](https://docs.astral.sh/uv/) (recommended):

```bash
uv sync
```

Or with pip:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Add your keys

```bash
cp .env.example .env
```

Open `.env` and fill in **only the keys for the frameworks you want to try**:

| To run | You need | Where to get it |
|---|---|---|
| Google ADK + Gemini | `GOOGLE_API_KEY` | [Google AI Studio](https://aistudio.google.com/apikey) (free tier) |
| OpenAI Agents SDK, or Google ADK + OpenAI | `OPENAI_API_KEY` | [OpenAI Platform](https://platform.openai.com/api-keys) |
| Microsoft Agent Framework, or Google ADK + Azure | `AZURE_OPENAI_*` | Azure Portal → your Azure OpenAI resource |
| AWS Strands | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | AWS IAM, plus model access turned on in the Bedrock console |

### Step 3: Run

| Framework | Command |
|---|---|
| Google ADK (chat page at http://127.0.0.1:8000) | `uv run adk web` |
| Google ADK (terminal) | `uv run adk run google_adk_agent` |
| OpenAI Agents SDK | `uv run python openai_adk_agent.py` |
| AWS Strands Agents | `uv run python aws_adk_agent.py` |
| Microsoft Agent Framework | `uv run python azure_adk_agent.py` |

Type `exit` to stop. Using pip? Leave out `uv run`.

For Google ADK, choose the model with `MODEL_PROVIDER=gemini`, `openai` or `azure` in `.env`.

**Try asking:**
- *What time is it in Tokyo?*
- *And in New York?* (tests memory)
- *What's the time?* (no city – the agent should ask you which one)

---

## 7. Project files

```
.
├── google_adk_agent/          # Google ADK
│   ├── __init__.py            #   picks the model using MODEL_PROVIDER
│   ├── gemini_agent.py        #   Google ADK + Gemini
│   ├── openai_agent.py        #   Google ADK + OpenAI (via LiteLLM)
│   └── azure_agent.py         #   Google ADK + Azure OpenAI (via LiteLLM)
├── openai_adk_agent.py        # OpenAI Agents SDK
├── aws_adk_agent.py           # AWS Strands Agents
├── azure_adk_agent.py         # Microsoft Agent Framework
├── .env.example               # template for your keys (copy to .env)
├── requirements.txt           # packages for pip
└── pyproject.toml / uv.lock   # packages for uv
```

---

## 8. Glossary

| Word | Simple meaning |
|---|---|
| **LLM** | Large Language Model, the AI "brain" that reads and writes text (Gemini, GPT, Claude). |
| **Agent** | An LLM that can use tools to get things done, not just chat. |
| **ADK / SDK** | Agent Development Kit / Software Development Kit: a library that makes building something easier. |
| **Tool / Function calling** | Letting the model ask your code to run a function and give it the result. |
| **Instructions / System prompt** | Hidden rules that tell the agent how to behave. |
| **Runner** | The part that runs the agent loop: question → tool → answer. |
| **Agent loop** | Repeat: model thinks → maybe calls a tool → reads result → until it has a final answer. |
| **Session** | The saved conversation, so the agent remembers earlier messages. |
| **LiteLLM** | A library that lets one framework talk to many model providers with the same code. |
| **Bedrock** | AWS's service for using AI models (like Claude) inside AWS. |
| **Azure OpenAI** | OpenAI models hosted on Microsoft Azure. |
| **Deployment** | In Azure, the name you gave your copy of a model (e.g. `gpt-4o-mini`). |
| **API key** | A secret password that lets your code use a paid AI service. Keep it in `.env`. |
| **`.env` file** | A local file that holds your secret keys. Never commit it to Git. |
| **IANA time zone** | Standard time-zone names like `Asia/Kolkata` or `America/New_York`. |
| **async / await** | Python's way to wait for slow things (like a network call) without freezing. |

---

## 9. Practice exercises

Try these to check your understanding. Start with the framework you like most.

1. **Change the instructions.** Make the agent answer like a pirate. Only the instruction text changes.
2. **Add a second tool.** Write `get_weekday(timezone: str) -> str` and add it to `tools=[...]`.
   Ask *"What day is it in Sydney?"*
3. **Break the docstring.** Delete the tool's docstring and see whether the agent still uses it
   correctly. (This shows why docstrings matter.)
4. **Switch models.** In Google ADK, change `MODEL_PROVIDER` in `.env` and compare the answers.
5. **Port a tool.** Take your new tool from exercise 2 and add it to all four frameworks.
   Notice how little changes.

---

## 10. Common problems

| Problem | Fix |
|---|---|
| `GOOGLE_API_KEY` / `OPENAI_API_KEY` not found | Make sure `.env` is in the **project root** (next to this README), not inside a subfolder. |
| `adk web` shows no agent | Run it from the project root. The agent folder must contain `root_agent`. |
| Azure: "deployment not found" | `AZURE_OPENAI_DEPLOYMENT` must match the deployment name in your Azure portal exactly. |
| AWS: "AccessDeniedException" | Turn on access to the model in the **Bedrock console → Model access**, and check `AWS_REGION`. |
| Model name not found | Model names change often. Set a current one in `.env` (`GEMINI_MODEL`, `OPENAI_MODEL`, `AWS_BEDROCK_MODEL`). |

---

## Learn more

- Google ADK: https://google.github.io/adk-docs/
- OpenAI Agents SDK: https://openai.github.io/openai-agents-python/
- AWS Strands Agents: https://strandsagents.com/
- Microsoft Agent Framework: https://learn.microsoft.com/agent-framework/
