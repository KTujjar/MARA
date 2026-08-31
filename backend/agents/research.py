from tools.local_search import search_local_docs
from tools.web_search import web_search
import anthropic

client = anthropic.Anthropic()

TOOLS = [
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

def run_research_agent(user_query : str, max_iterations : int=8) -> str:
    messages = [{"role": "user", "content": user_query}]

    for i in range(max_iterations):
        response = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=1024,
            tools = TOOLS,
            messages = messages,
        )
        
        messages.append({"role": "assistant", "content": response.content})

        tool_calls = [b for b in response.content if b.type == "tool_use"]
        if not tool_calls:
            return "".join(b.text for b in response.content if b.type == "text")
        tool_results = []
        for block in tool_calls:
            if block.name == "web_search":
                print(f"\n\n\n🔍 Calling web_search with query: {block.input['query']}\n\n\n")  # add this
                result = web_search(block.input["query"])
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result)
                })
            if block.name == "local_search":
                print(f"\n\n\n🔍 Calling local_search with query: {block.input['query']}\n\n\n")  # add this
                result = search_local_docs(block.input["query"])
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result)
                })

        messages.append({"role": "user", "content": tool_results})
        return "Reached max iterations without a final answer."
