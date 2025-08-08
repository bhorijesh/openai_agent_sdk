import os
from dotenv import load_dotenv
from agents import Agent, Runner
import asyncio

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Set the OpenAI API key in the environment for the agents SDK
if OPENAI_API_KEY:
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

Max_Tokens = 32768  

def create_agent(name: str, instructions: str) -> Agent | None:
    """Create an agent with the given name and instructions."""
    if not OPENAI_API_KEY:
        return None
    
    return Agent(
        name=name,
        instructions=instructions,
    )

async def call_openai_agent(agent: Agent, prompt: str) -> str:
    """Run an agent with the given prompt."""
    if not agent:
        return "[OpenAI API key missing]"
    
    try:
        result = await Runner.run(agent, prompt)
        return result.final_output
    except Exception as e:
        return f"[Error calling OpenAI Agents API: {str(e)}]"

def call_openai_sync(agent: Agent, prompt: str) -> str:
    """Synchronous wrapper for calling OpenAI agent."""
    return asyncio.run(call_openai_agent(agent, prompt))

# Legacy function for backward compatibility
def call_openai(messages, model="gpt-4.1-mini", temperature=0.7, max_tokens=Max_Tokens):
    """Legacy function - converts messages to prompt and uses basic agent."""
    if not OPENAI_API_KEY:
        return "[OpenAI API key missing]"
    
    # Convert messages to a single prompt
    prompt = ""
    for msg in messages:
        if msg["role"] == "system":
            prompt += f"System: {msg['content']}\n"
        elif msg["role"] == "user":
            prompt += f"User: {msg['content']}\n"
    
    # Create a basic agent for this call
    basic_agent = create_agent(
        name="Basic Agent",
        instructions="You are a helpful assistant. Follow the system instructions and respond to the user query."
    )
    
    if not basic_agent:
        return "[OpenAI API key missing]"
    
    return call_openai_sync(basic_agent, prompt)
