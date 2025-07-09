# main.py
import os
import asyncio
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from tools.weather_tool import get_weather

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
load_dotenv()

# Step 1: Setup LLM via OpenRouter
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="mistralai/mistral-7b-instruct"
)

# Step 2: Setup tools
tools = [get_weather]

# Step 3: Create a LangGraph ReAct agent
agent = create_react_agent(model=llm, tools=tools)

# Step 4: Run the agent asynchronously with user input
async def run_agent(query: str, session_id: str = "default"):
    """Run the agent with the given query and session ID."""
    logger.info(f"Processing query: {query}")

    state = {
        "messages": [HumanMessage(content=query)],
        "session_id": session_id
    }

    try:
        response = await agent.ainvoke(state)
        logger.info(f"Raw response: {response}")
        if isinstance(response, dict) and "messages" in response:
            messages = response["messages"]
            final_message = None
            for msg in reversed(messages):
                if isinstance(msg, AIMessage) and msg.content and msg.content.strip() and "[TOOL_CALLS]" not in msg.content:
                    final_message = msg.content.strip()
                    break
            if not final_message:
                for msg in reversed(messages):
                    if isinstance(msg, ToolMessage):
                        final_message = msg.content.strip()
                        break
            if not final_message:
                final_message = "No response content found"

            for msg in messages:
                if isinstance(msg, AIMessage) and hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        logger.info(f"Tool used: {tool_call['name']} with input {tool_call['args']}")
        elif isinstance(response, AIMessage):
            final_message = response.content.strip() if response.content and "[TOOL_CALLS]" not in response.content else "No response content found"
            if hasattr(response, "tool_calls") and response.tool_calls:
                for tool_call in response.tool_calls:
                    logger.info(f"Tool used: {tool_call['name']} with input {tool_call['args']}")
        else:
            final_message = "Unexpected response format"
            logger.warning(f"Unexpected response type: {type(response)}")

        logger.info(f"Agent response: {final_message}")
        return final_message
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return f"Error: {str(e)}"

async def main():
    print("Welcome to the Weather Agent! Type 'exit' to quit.")

    while True:
        user_input = input("Enter your query: ")
        if user_input.lower() == "exit":
            break

        response = await run_agent(user_input)
        print(f"Agent: {response}\n")

if __name__ == "__main__":
    asyncio.run(main())