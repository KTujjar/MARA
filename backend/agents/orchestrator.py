import anthropic
from anthropic.types import MessageParam
from langsmith.wrappers import wrap_anthropic

from graph.state import ResearchState

client = wrap_anthropic(anthropic.Anthropic())

def orchestrator_node(state: ResearchState) -> dict:
    """Break the user's query into a short research plan the 
    research agent can follow. Runs once at the start of the graph."""

    messages: list[MessageParam]=[{
        "role":"user",
        "content": (
            f"A user asked: {state['query']}\n\n"
            "write a short research plan (3-5 bullet points"
            " describing what needs to be investigated"
            " to answer this well. Just the plan, no preamble."
        ),
    }]


    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=512,
        messages = messages,
    )
    plan = "".join(b.text for b in response.content if b.type == "text")

    return {"plan":plan, "findings":[], "research_rounds":0}
