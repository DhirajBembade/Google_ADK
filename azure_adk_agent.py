"""City time agent built with Microsoft Agent Framework (packages: agent-framework-core,
agent-framework-openai). It replaces Semantic Kernel and AutoGen.

Run: uv run python azure_adk_agent.py
Needs the AZURE_OPENAI_* settings in .env
"""
import asyncio
import os
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from agent_framework import Agent, tool
from agent_framework.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

load_dotenv()

# 1. Tool: a normal Python function. @tool turns it into a tool the model can call.
@tool
def get_current_time(city: str, timezone: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city: The city name, e.g. "Mumbai".
        timezone: The IANA time zone for that city, e.g. "Asia/Kolkata",
            "America/New_York", "Europe/London".
    """
    try:
        now = datetime.now(ZoneInfo(timezone))
    except (ZoneInfoNotFoundError, ValueError):
        return {"status": "error", "error_message": f"Unknown time zone '{timezone}' for {city}."}
    return {
        "status": "success",
        "city": city,
        "timezone": timezone,
        "time": now.strftime("%I:%M %p"),
        "date": now.strftime("%A, %d %B %Y"),
        "utc_offset": now.strftime("%z"),
    }

# 2. Agent: client (Azure OpenAI) + instructions + tools.
agent = Agent(
    client=OpenAIChatCompletionClient(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    ),
    name="time_agent",
    instructions=(
        "You are a helpful assistant that tells the current time in cities. "
        "Always use the 'get_current_time' tool, passing the city and its IANA time zone "
        "(e.g. Mumbai -> Asia/Kolkata). Never guess the time yourself. "
        "If the user doesn't name a city, or the name is ambiguous, ask which city they mean."
    ),
    tools=[get_current_time],
)

# 3. Run: a session keeps the chat history between questions.
async def main() -> None:
    print("Microsoft Agent Framework (Azure) - type 'exit' to quit.")
    session = agent.create_session()
    while (question := input("\nYou: ").strip()).lower() not in {"exit", "quit"}:
        response = await agent.run(question, session=session)
        print("Agent:", response.text)


if __name__ == "__main__":
    asyncio.run(main())
