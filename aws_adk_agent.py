"""City time agent built with AWS Strands Agents (package: strands-agents).

Run: uv run python aws_adk_agent.py
Needs AWS credentials in .env and Bedrock model access in your AWS account.
"""
import os
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from dotenv import load_dotenv
from strands import Agent, tool
from strands.models import BedrockModel

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

# 2. Agent: model (Amazon Bedrock) + instructions + tools.
agent = Agent(
    model=BedrockModel(
        model_id=os.getenv("AWS_BEDROCK_MODEL", "global.anthropic.claude-sonnet-4-6"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    ),
    system_prompt=(
        "You are a helpful assistant that tells the current time in cities. "
        "Always use the 'get_current_time' tool, passing the city and its IANA time zone "
        "(e.g. Mumbai -> Asia/Kolkata). Never guess the time yourself. "
        "If the user doesn't name a city, or the name is ambiguous, ask which city they mean."
    ),
    tools=[get_current_time],
    callback_handler=None,  # don't stream text to the screen; we print the final answer
)

# 3. Run: just call the agent. It remembers the chat history by itself.
if __name__ == "__main__":
    print("AWS Strands Agents - type 'exit' to quit.")
    while (question := input("\nYou: ").strip()).lower() not in {"exit", "quit"}:
        print("Agent:", agent(question))
