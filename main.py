import os
import operator
from datetime import datetime, timezone
from typing import TypedDict, Annotated, List, Union
from dotenv import load_dotenv

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

load_dotenv()


@tool
def get_current_time() -> dict:
    """Возвращает текущее время UTC в формате ISO-8601.
    Пример → {"utc": "2025-05-21T06:42:00Z"}"""
    now_utc = datetime.now(timezone.utc)
    return {"utc": now_utc.isoformat(timespec='seconds').replace('+00:00', 'Z')}

tools = [get_current_time]
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0)
model_with_tools = model.bind_tools(tools)

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]

def agent_node(state: AgentState) -> dict:
    print("---AGENT NODE---")
    response = model_with_tools.invoke(state["messages"])
    return {"messages": [response]}
tool_node = ToolNode(tools)


def should_continue_node(state: AgentState) -> str:
    print("---SHOULD CONTINUE NODE---")
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        print(f"Decision: Call tool {last_message.tool_calls[0]['name']}")
        return "tool_node"
    print("Decision: End")
    return END


workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tool_node", tool_node)
workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue_node,
    {
        "tool_node": "tool_node",
        END: END,
    },
)

workflow.add_edge("tool_node", "agent")
app = workflow.compile()
