from langchain.tools import tool

@tool
def knowledge_base(query: str) -> str:
    """Searches the knowledge base for information."""
    with open("customer_support/knowledge_base.txt", "r") as f:
        lines = f.readlines()

    matching_lines = [line.strip() for line in lines if query.lower() in line.lower()]

    if matching_lines:
        return "\\n".join(matching_lines)
    else:
        return "I'm sorry, I don't have information about that."
