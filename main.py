from langchain_core.messages import (
    BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
)
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from pathlib import Path
from state import AgentState
from tools.tools_funcation import  (make_dir,pdf_move_category,rename_pdf,read_pdf,update_currpdf)
from typing_extensions import TypedDict
from pathlib import Path




tools =[make_dir,pdf_move_category,rename_pdf,read_pdf,update_currpdf]

model = ChatOpenAI(
    model="",  #enter model
    openai_api_key="", #enter api
    base_url="https://openrouter.ai/api/v1",
).bind_tools(tools)



#-------------------------------------------------------------
# ✅ Function Of First Node 
# to collect content of dirctory
#-------------------------------------------------------------
def collect_files(state:AgentState)->AgentState:
    fpath =Path(state['dir'])
    state['pdf_files']=list(fpath.glob("*.pdf"))
    return state




from langchain_core.messages import SystemMessage, AIMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables import RunnableConfig
from state import AgentState
from typing import cast

def our_agent(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content="""
    You are a smart PDF organization assistant. Your task is to sort, rename, and organize PDF files found in the directory provided in state['dir'].

    Here's what you should do step-by-step:

    1. The list of PDF filenames to process is in `state['pdf_files']`. You will handle them one by one. For each file:
    - Temporarily store the file's name in `state['pdf_curr']`.
    - Read its content. The text content of the current file will be found in `state['content']`.

    2. From the content of the file, try to understand:
    - The correct title of the book or document.
    - Its topic or subject area (e.g., physics, chemistry, mathematics, philosophy, etc.).

    3. If the filename is already correct (i.e., it matches the actual title of the document), **do nothing** to the name.  
    Otherwise, **rename the file** to match the correct title you found from the content.

    4. Once you know the topic of the document:
    - Check if a folder for that topic (e.g., `physics/`, `chemistry/`) exists in `state['dir']`.
    - If it doesn't exist, **create it**.
    - Then move the file into that folder.

    5. After processing the current file:
    - Remove its name from `state['pdf_files']`.
    - Go to the next file in the list.

     Tips for determining the title and subject:
    - Titles are usually written on the first page in large or bold text.
    - Subjects can often be guessed from repeated keywords in the introduction or chapter titles.

     Example 1:
    - Filename: "book_123.pdf"
    - Content: "Quantum Mechanics: An Introduction by David Griffiths"
    - → Rename to: "Quantum Mechanics - David Griffiths.pdf"
    - → Move to: "physics/"

     Example 2:
    - Filename: "ABC001.pdf"
    - Content: "Organic Chemistry, 9th Edition by John McMurry"
    - → Rename to: "Organic Chemistry - John McMurry.pdf"
    - → Move to: "chemistry/"

     Notes:
    - Only work inside the directory given in state['dir'].
    - Never delete any file, only rename and move.
    - Base your decisions on the content in state['content'] only.
    """)

    # build all messages (system + conversation)
    all_messages = [system_prompt] + list(state["messages"])

    # get LLM response
    response = model.invoke(all_messages)

    print(f"\n AI: {response.content}")
    if hasattr(response, "tool_calls") and response.tool_calls:
        print(f" USING TOOLS: {[tc['name'] for tc in response.tool_calls]}")

    # append AI message to history
    state["messages"].append(cast(AIMessage, response))
    
    return state



def should_continue(state: AgentState) -> str:
    """Determine if we should continue or end the conversation."""

    messages = state["messages"]
    
    if not messages:
        return "continue"
    
    if state['pdf_files']:
        return "continue"
    else:
        print("FINISHED")
        return "stop"


graph = StateGraph(AgentState)

graph.add_node('collection',collect_files)
graph.add_node("agent", our_agent)
graph.add_node("tools", ToolNode(tools))

graph.add_edge('collection','agent')
graph.add_edge('agent','tools')

graph.set_entry_point("collection")

graph.add_conditional_edges(
    "tools",
    should_continue,
    {
        "continue":"agent",
        "stop":END
    }
)

app = graph.compile()


app.invoke({'dir':r"C:\Users\mohamed\Desktop\books"})



