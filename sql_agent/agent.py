from langchain_anthropic import ChatAnthropic
from deepagents import create_deep_agent

from sql_agent.prompts import SQL_AGENT_INSTRUCTIONS
from sql_agent.tools import sql_runner

# Model Claude 3 Sonnet
model = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.0)

# Create the agent
agent = create_deep_agent(
    model=model,
    tools=[sql_runner],
    system_prompt=SQL_AGENT_INSTRUCTIONS,
)
