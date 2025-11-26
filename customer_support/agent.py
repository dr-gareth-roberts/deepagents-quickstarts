from langchain_anthropic import ChatAnthropic
from deepagents import create_deep_agent

from customer_support.prompts import CUSTOMER_SUPPORT_INSTRUCTIONS
from customer_support.tools import knowledge_base

# Model Claude 3 Sonnet
model = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.0)

# Create the agent
agent = create_deep_agent(
    model=model,
    tools=[knowledge_base],
    system_prompt=CUSTOMER_SUPPORT_INSTRUCTIONS,
)
