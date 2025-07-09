# Coding Test: Build a Weather Agent with LangGraph and OpenRouter

## Objective

The purpose of this coding test is to evaluate your ability to:

- Use OpenRouter to connect to an LLM
- Build a custom tool and integrate it with a LangGraph agent
- Apply the ReAct agent pattern using LangGraph
- Handle asynchronous execution

## Project Requirements

You are required to:

1. Set up OpenRouter LLM integration:
   - Use `ChatOpenAI` with `base_url="https://openrouter.ai/api/v1"`
   - Set the API key using a `.env` file
   - Use a supported model, for example `"mistralai/mistral-7b-instruct"`

2. Implement a fake weather tool:
   - Create a function with the signature `def get_weather(city: str) -> str`
   - Return a fake weather string such as `"The weather in {city} is sunny and 25°C."`
   - Register the tool using the `@tool` decorator

3. Build the agent using LangGraph:
   - Use `create_react_agent()` from `langgraph.prebuilt`
   - Connect the tool using `ToolExecutor`
   - The agent should:
     - Accept natural language input
     - Decide whether to use the tool or reply directly
     - Return a final response

4. Add user interaction:
   - Prompt the user to input a question
   - Run the agent and print the output

## Bonus (Optional)

- Use asyncio to run the agent with `await agent.ainvoke(...)`
- Add logging to show tool usage
- Add simple memory or state management

## Sample Inputs

- "What’s the weather like in Tokyo?" → should trigger the weather tool
- "Hi there!" → should respond directly without using the tool

## Setup Instructions

1. Make sure Python 3.8+ is installed
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory:

```
OPENROUTER_API_KEY=your_key_here
```

4. Run the application:

```bash
python main.py
```

## Files Provided

- `main.py`: Entry point for your agent logic
- `tools/weather_tool.py`: Template for the fake weather tool
- `requirements.txt`: List of dependencies
- `README.md`: This instruction file

## Submission Guidelines

- The provided files are for reference only. You are welcome to make any modification by yourself
- The code should be clean and runnable
- The agent should produce a valid response when given a weather-related or casual query
- Ensure OpenRouter and LangGraph are properly integrated
