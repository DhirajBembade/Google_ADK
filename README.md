# Google ADK – City Time Agent

A small AI agent built with [Google ADK](https://google.github.io/adk-docs/).
Ask it "What time is it in Tokyo?" and it tells you the current time there.

It can run on either:
- **Gemini** (Google) – `my_agent/gcp_agent.py`
- **OpenAI** – `my_agent/openai_agent.py`
- **Azure OpenAI** – `my_agent/azure_agent.py`

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
cp my_agent/.env.example my_agent/.env
```

Open `my_agent/.env` and fill in:
- `MODEL_PROVIDER` – `gemini`, `openai` or `azure`
- For Gemini: `GOOGLE_API_KEY` (free key from [Google AI Studio](https://aistudio.google.com/apikey))
- For OpenAI: `OPENAI_API_KEY` (from [OpenAI](https://platform.openai.com/api-keys))
- For Azure: your Azure OpenAI key, endpoint and deployment name

## 3. Run

Run these from the project folder:

```bash
uv run adk web            # opens a chat page at http://127.0.0.1:8000
uv run adk run my_agent   # chat in the terminal
```

(Using pip? Drop `uv run` and just type `adk web` or `adk run my_agent`.)

## Project files

```
my_agent/
  __init__.py      # picks Gemini, OpenAI or Azure based on MODEL_PROVIDER
  gcp_agent.py     # agent using Gemini
  openai_agent.py  # agent using OpenAI
  azure_agent.py   # agent using Azure OpenAI
  .env.example     # sample settings – copy to .env
```
