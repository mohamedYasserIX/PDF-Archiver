# state.py
from typing import Annotated, Sequence#, TypedDict
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

# -------------------------------
# ✅ Agent State Definition
# -------------------------------
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    dir: str
    pdf_files: list[str]
    pdf_curr: str
    content: list[str]
    category: list[str]