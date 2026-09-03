import json
import anthropic
from anthropic.types import MessageParam
from langsmith.wrappers import wrap_anthropic


from graph.state import ResearchState

client = wrap_anthropic(anthropic.Anthropic())

#so the research/critique loop doesnt loop forever
MAX_RESEARCH_ROUNDS = 2

def critique_node(state:ResearchState)->dict:
    #Check the accumulated findings against the original question
    #Sets needs_more_research to route the graph back to research original
    #lets it fall through to the writer.

    findings_text = "\n\n---\n\n".join(state.get("findings", []))

    messages: list[MessageParam]=[{
        "role":"user",
        "content":(
            f"Original question: {state['query']}\n\n"
            f"Research findings so far:\n{findings_text}\n\n"
            "Do these findings sufficiently answer the question with "
            "credible, specific evidence? Reply with ONLY a JSON object, "
            'no other text: {"sufficient": true or false, '
            '"notes": "what is missing, if anything"}'
        ),
    }]
    
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=512,
        messages=messages,
    )
    text = "".join(b.text for b in response.content if b.type == "text")

    try:
        verdict = json.loads(text)
    except json.JSONDecodeError:
        #doesnt risk infinite loop if JSON is not clean
        verdict = {"sufficient":True, "notes": ""}
    
    if state.get("research_rounds", 0) >= MAX_RESEARCH_ROUNDS:
        verdict["sufficient"] = True

    return {
        "needs_more_research": not verdict.get("sufficient", True),
        "critique_notes": verdict.get("notes",""),
    }
