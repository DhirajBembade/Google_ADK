"""City time agent built with the OpenAI Agents SDK (package: openai-agents).

Run: uv run python openai_adk_agent.py
Needs OPENAI_API_KEY in .env
"""
import os
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from agents import Agent, Runner, function_tool
from dotenv import load_dotenv

load_dotenv()

# 1. Tool: a normal Python function. @function_tool turns it into a tool the model can call.
@function_tool
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

# 2. Agent: model + instructions + tools.
agent = Agent(
    name="time_agent",
    model=os.getenv("OPENAI_MODEL", "gpt-6-astra"),
    instructions=(
        "You are a helpful assistant that tells the current time in cities. "
        "Always use the 'get_current_time' tool, passing the city and its IANA time zone "
        "(e.g. Mumbai -> Asia/Kolkata). Never guess the time yourself. "
        "If the user doesn't name a city, or the name is ambiguous, ask which city they mean."
    ),
    tools=[get_current_time],
)

# 3. Runner: sends the question, runs any tool calls, returns the final answer.
if __name__ == "__main__":
    print("OpenAI Agents SDK - type 'exit' to quit.")
    history = []
    while (question := input("\nYou: ").strip()).lower() not in {"exit", "quit"}:
        result = Runner.run_sync(agent, history + [{"role": "user", "content": question}])
        print("Agent:", result.final_output)
        history = result.to_input_list()  # keep the chat history for the next turn
