import os
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

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

root_agent = Agent(
    model=LiteLlm(
        model=f"azure/{os.getenv('AZURE_OPENAI_DEPLOYMENT')}",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    ),
    name='root_agent',
    description="Tells the current time in a specified city.",
    instruction=(
        "You are a helpful assistant that tells the current time in cities. "
        "Always use the 'get_current_time' tool, passing the city and its IANA time zone "
        "(e.g. Mumbai -> Asia/Kolkata). Never guess the time yourself. "
        "If the user doesn't name a city, or the name is ambiguous, ask which city they mean."
    ),
    tools=[get_current_time],
)
