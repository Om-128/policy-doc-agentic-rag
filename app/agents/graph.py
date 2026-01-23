import time

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

# Decision Node
def decide_tool(state : AgentState) -> AgentState:
    print("👉 DECIDE NODE CALLED")

    probe_result = vector_tool.store.similarity_search_with_relevance_scores(
        state["question"],
        k=1
    )

    if probe_result:
        _, score = probe_result[0]
    else:
        score = 0.0
    
    prompt = f"""
Decide which tool should be used to answer the question.

Vector store relevance score for this question: {score}

Rules:
- If relevance score >= 0.3 → use VECTOR
- If relevance score < 0.3 → use WEB

Respond with only one word: vector or web.

Question:
{state["question"]}
"""
    decision = llm.invoke(prompt).content.strip().lower()
    return {"decision": decision}


# Vector search node
def vector_node(state: AgentState) -> AgentState:
    print("📘 VECTOR NODE CALLED")
    chunks = vector_tool.run(state["question"])

    if not chunks:
        chunks = web_tool.run(state["question"])
        source = "web_search"
    else:
        source = "vector_search"

    state["chunks"] = chunks
    state["source"] = source
    return state

# Web Search Node
# -------------------------
def web_node(state: AgentState) -> AgentState:
    print("🌐 WEB NODE CALLED")
    state["chunks"] = web_tool.run(state["question"])
    state["source"] = "web_search"
    return state


# Answer Node
def answer_node(state: AgentState) -> AgentState:
    print("✍️ ANSWER NODE CALLED")
    prompt = f"""
Answer the question using ONLY the context below.

Context:
{state['chunks']}

Question:
{state['question']}
"""

    state["answer_prompt"] = prompt
    return state

# Build Graph
graph = StateGraph(AgentState)

graph.add_node("decide", decide_tool)
graph.add_node("vector", vector_node)
graph.add_node("web", web_node)
graph.add_node("answer", answer_node)

graph.set_entry_point("decide")

graph.add_conditional_edges(    
    "decide",
    lambda state: state["decision"],
    {
        "vector": "vector",
        "web": "web",
    }
)

graph.add_edge("vector", "answer")
graph.add_edge("web", "answer")
graph.add_edge("answer", END)

app = graph.compile()