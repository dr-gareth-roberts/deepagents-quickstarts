from langchain_anthropic import ChatAnthropic
from deepagents import create_deep_agent

from code_generation.prompts import CODE_GENERATION_INSTRUCTIONS
from code_generation.tools import python_repl

# Model Claude 3 Sonnet
model = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.0)

# Create the agent
agent = create_deep_agent(
    model=model,
    tools=[python_repl],
    system_prompt=CODE_GENERATION_INSTRUCTIONS,
)
