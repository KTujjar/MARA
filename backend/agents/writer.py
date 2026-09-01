import anthropic
from anthropic.types import MessageParam

from graph.state import ResearchState

client = anthropic.Anthropic()

def writer_node(state:ResearchState)->dict:
    #Synthesize findings into a final Markdown report.
    findings_text = "\n\n---\n\n".join(state.get("findings", []))

    messages:list[MessageParam] = [{
        "role":"user",
        "content":(
            f"Original question: {state['query']}\n\n"
            f"Research findings:\n{findings_text}\n\n"
            "Write a clear, well-organized report answering the "
            "question using these findings. Use Markdown."
        ),
    }]
    
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1500,
        messages=messages,
    )

    report = "".join(b.text for b in response.content if b.type == "text")

    return {"report":report}
