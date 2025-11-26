from langchain.tools import tool
import sqlite3

@tool
def sql_runner(query: str) -> str:
    """Executes a SQL query against the products database."""
    conn = sqlite3.connect("sql_agent/products.db")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return str(results)
