import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from graph.build_graph import build_graph

router = APIRouter()
graph = build_graph()

class QueryRequest(BaseModel):
    query:str

def event_stream(query: str):
    try:
        for update in graph.stream({"query": query}, stream_mode="updates"):
            for node_name, node_output in update.items():
                payload = {"node": node_name, "output": node_output}
                yield f"data: {json.dumps(payload)}\n\n"
        yield "event: done\ndate: {}\n\n"
    except Exception as e:
        yield f"event: error\ndata: {json.dumps({'message': str(e)})}\n\n"

@router.post("/query")
def query_endpoint(req: QueryRequest):
    return StreamingResponse(event_stream(req.query), media_type="text/event-stream")
