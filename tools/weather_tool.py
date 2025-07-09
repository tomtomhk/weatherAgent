# tools/weather_tool.py
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Fake weather lookup for the given city."""
    return f"The weather in {city} is sunny and 25°C."