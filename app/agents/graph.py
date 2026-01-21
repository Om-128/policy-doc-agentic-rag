from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq

from app.agents.state import AgentState
from app.agents.tools.vector_search_tool import VectorSearchTool
from app.agents.tools.web_search_tool import WebSearchTool

# Initialize LLM
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

vector_tool = VectorSearchTool()
web_tool = WebSearchTool()