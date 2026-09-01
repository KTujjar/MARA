from langgraph.graph import StateGraph, END

from graph.state import ResearchState
from agents.orchestrator import orchestrator_node
from agents.research import research_node
from agents.critique import critique_node
from agents.writer import writer_node

def route_after_critique(state:ResearchState)->str:
    return "research" if state.get("needs_more_research") else "writer"

def build_graph():
    graph=StateGraph(ResearchState)
    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("research", research_node)
    graph.add_node("critique", critique_node)
    graph.add_node("writer",writer_node)

    graph.set_entry_point("orchestrator")
    graph.add_edge("orchestrator","research")
    graph.add_edge("research", "critique")
    graph.add_conditional_edges(
        "critique",
        route_after_critique,
        {"research": "research", "writer":"writer"},
    )
    graph.add_edge("writer",END)

    return graph.compile()
