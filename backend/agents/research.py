from agents.critique import critique_node
from graph.state import ResearchState
from tools.local_search import search_local_docs
from tools.web_search import web_search
import anthropic
from anthropic.types import ToolParam, MessageParam, ToolResultBlockParam 
from typing import Any, cast

client = anthropic.Anthropic()

TOOLS:list[ToolParam] = [
    {
        "name": "web_search",
        "description": "Search the web for current information",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        }
    },
    {
        "name": "local_search",
        "description": "Search through local files for current information",
        "input_schema": {
            "type": "object",
            "properties":{
                "query":{"type":"string", "description": "the search query"}
            },
            "required":["query"]
        }
    },
]

def research_node(state: ResearchState, max_iterations : int=8) -> dict:

    prompt = f"Research plan:\n{state.get('plan','')}\n\n"
    
    if state.get("critique_notes"):
        prompt += (
            f"A previous review flagged these gaps - focus on closing them:\n"
            f"{state.get('critique_notes','')}\n\n"
        )
    prompt += f"Original question: {state['query']}"

    messages: list[MessageParam] = [{"role": "user", "content": prompt}]

    for _ in range(max_iterations):
        response = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=1024,
            tools = TOOLS,
            messages = messages,
        )
        
        messages.append({"role": "assistant", "content": response.content})

        tool_calls = [b for b in response.content if b.type == "tool_use"]
        if not tool_calls:
            summary = "".join(b.text for b in response.content if b.type == "text")
            findings = state.get("findings", []) + [summary]
            return {
                "findings": findings,
                "research_rounds": state.get("research_rounds", 0) + 1,
            }

        tool_results: list[ToolResultBlockParam] = []
        for block in tool_calls:

            tool_input = cast(dict[str, Any], block.input)

            if block.name == "web_search":
                print(f"\n\n\n🔍 Calling web_search with query: {block.input['query']}\n\n\n")  # add this
                result = web_search(tool_input["query"])
            elif block.name == "local_search":
                print(f"\n\n\n🔍 Calling local_search with query: {block.input['query']}\n\n\n")  # add this
                result = search_local_docs(tool_input["query"])
            else:
                result = f"Unknown tool: {block.name}"

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": str(result)
            })

        messages.append({"role": "user", "content": tool_results})
    
    findings = state.get("findings", []) + [
        "Reached max iterations without a final resaerch sumamry."
    ]
    return {"findings": findings, "research_rounds": state.get("research_rounds", 0) + 1}
