#!/usr/bin/env python3
"""Standalone script to run the deep research agent.

This script demonstrates how to use the deepagents package to build a research
agent with custom tools for web search and strategic thinking.

Usage:
    python run_research.py "Your research question here"
"""

import os
import sys
from datetime import datetime

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from rich.console import Console
from rich.panel import Panel

from deepagents import create_deep_agent
from research_agent.prompts import (
    FILE_USAGE_INSTRUCTIONS,
    RESEARCHER_INSTRUCTIONS,
    SUBAGENT_USAGE_INSTRUCTIONS,
    TODO_USAGE_INSTRUCTIONS,
)
from research_agent.tools import tavily_search, think_tool
from utils import format_messages

# Initialize console for rich output
console = Console()

# Load environment variables from parent directory
load_dotenv(os.path.join("..", ".env"), override=True)


def create_research_agent():
    """Create and configure the deep research agent.

    Returns:
        Configured LangGraph agent ready for research tasks
    """
    # Initialize model
    model = init_chat_model(model="anthropic:claude-sonnet-4-20250514", temperature=0.0)

    # Define agent limits
    max_concurrent_research_units = 3
    max_researcher_iterations = 3

    # Custom tools for research
    sub_agent_tools = [tavily_search, think_tool]

    # Configure research sub-agent
    research_sub_agent = {
        "name": "research-agent",
        "description": "Delegate research to the sub-agent researcher. Only give this researcher one topic at a time.",
        "prompt": RESEARCHER_INSTRUCTIONS,
        "tools": ["tavily_search", "think_tool"],
    }

    # Build main agent instructions
    instructions = (
        "# TODO MANAGEMENT\n"
        + TODO_USAGE_INSTRUCTIONS
        + "\n\n"
        + "=" * 80
        + "\n\n"
        + "# FILE SYSTEM USAGE\n"
        + FILE_USAGE_INSTRUCTIONS
        + "\n\n"
        + "=" * 80
        + "\n\n"
        + "# SUB-AGENT DELEGATION\n"
        + SUBAGENT_USAGE_INSTRUCTIONS
    )

    # Create deep agent
    agent = create_deep_agent(
        sub_agent_tools,
        instructions,
        subagents=[research_sub_agent],
        model=model,
    )

    return agent


def run_research(query: str):
    """Run research on the given query.

    Args:
        query: The research question to investigate
    """
    console.print(
        Panel(
            f"[bold cyan]Research Query:[/bold cyan] {query}",
            title="Deep Research Agent",
            border_style="cyan",
        )
    )
    console.print("\n[yellow]Initializing agent...[/yellow]\n")

    # Create agent
    agent = create_research_agent()

    # Run research
    console.print("[yellow]Starting research...[/yellow]\n")
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query,
                }
            ],
        }
    )

    # Display results
    console.print("\n[green]Research complete![/green]\n")
    console.print(Panel("Message History", style="bold magenta"))
    format_messages(result["messages"])


def main():
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        console.print(
            "[red]Error:[/red] Please provide a research query.\n\n"
            "[yellow]Usage:[/yellow]\n"
            "  python run_research.py \"Your research question here\"\n\n"
            "[yellow]Example:[/yellow]\n"
            '  python run_research.py "Give me a brief overview of Model Context Protocol (MCP)"'
        )
        sys.exit(1)

    # Get query from command line arguments
    query = " ".join(sys.argv[1:])

    # Run research
    run_research(query)


if __name__ == "__main__":
    main()
