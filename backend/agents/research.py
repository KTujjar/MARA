from tools.web_search import web_search
import anthropic

client = anthropic.Anthropic()

TOOLS = [{
    "name": "web_search",
    "description": "Search the web for current information",
    "input_schema": {
        "type": "object",
        "properties": {"query": {"type": "string"}},
        "required": ["query"],
    },
}]

def run_research_agent(user_query : str) -> str:
    messages = [{"role": "user", "content": user_query}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=1024,
            tools = TOOLS,
            messages = messages,
        )
        
        messages.append({"role": "assistant", "content": response.content})

        tools_calls = [b for b in response.content if b.type == "tool_use"]
        if not tools_calls:
            return "".join(b.text for b in response.content if b.type == "text")
        tool_results = []
        for block in tools_calls:
            if block.name == "web_search":
                result = web_search(block.input["query"])
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result)
                })
        messages.append({"role": "user", "content": tool_results})
