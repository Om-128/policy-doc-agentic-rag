from typing import TypedDict, List

class AgentState(TypedDict):
    question: str
    chunks: List[str]
    source: str
    decision: str
    answer_prompt: str