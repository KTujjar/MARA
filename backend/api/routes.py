import json
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import repository
from db.session import SessionLocal, get_db
from graph.build_graph import build_graph

router = APIRouter()
graph = build_graph()

DbSession = Annotated[Session, Depends(get_db)]

class QueryRequest(BaseModel):
    query:str

def event_stream(query: str, query_id: int, db: Session):
    """Streams graph updates as SSE events and persists them as they arrive.
 
    Owns its own DB session for the lifetime of the generator (see the note
    in db/session.py on why get_db()/Depends() can't be used here).
    """
    findings_seen = 0
    try:
        for update in graph.stream({"query": query}, stream_mode="updates"):
            for node_name, node_output in update.items():
                payload = {"node": node_name, "output": node_output}
                yield f"data: {json.dumps(payload)}\n\n"
 
                if node_name == "research":
                    findings = node_output.get("findings") or []
                    for finding in findings[findings_seen:]:
                        repository.add_finding(
                            db,
                            query_id,
                            round_number=node_output.get("research_rounds", 0),
                            content=finding,
                        )
                    findings_seen = len(findings)
 
                elif node_name == "critique":
                    repository.set_critique_notes(
                        db,
                        query_id,
                        notes=node_output.get("critique_notes", ""),
                        research_rounds=node_output.get("research_rounds", 0),
                    )
 
                elif node_name == "writer" and node_output.get("report"):
                    repository.save_report(db, query_id, node_output["report"])
 
        yield "event: done\ndata: {}\n\n"
    except Exception as e:
        repository.mark_failed(db, query_id, str(e))
        yield f"event: error\ndata: {json.dumps({'message': str(e)})}\n\n"
    finally:
        db.close()
 
 
@router.post("/query")
def query_endpoint(req: QueryRequest):
    # Short-lived session just to create the row and get an id back.
    with SessionLocal() as db:
        saved_query = repository.create_query(db, req.query)
 
    # Separate long-lived session, owned by the generator, that outlives
    # this request handler for as long as the stream is open.
    stream_db = SessionLocal()
    return StreamingResponse(
        event_stream(req.query, saved_query.id, stream_db),
        media_type="text/event-stream",
    )
 
 
@router.get("/history")
def history_endpoint(db: DbSession, limit: int = 20):
    queries = repository.list_history(db, limit=limit)
    return [
        {
            "id": q.id,
            "query": q.query_text,
            "status": q.status,
            "created_at": q.created_at.isoformat(),
            "completed_at": q.completed_at.isoformat() if q.completed_at else None,
        }
        for q in queries
    ]
 
 
@router.get("/reports/{query_id}")
def report_endpoint(query_id: int, db: DbSession):
    query = repository.get_query_with_report(db, query_id)
    if query is None:
        raise HTTPException(status_code=404, detail="Query not found")
    return {
        "id": query.id,
        "query": query.query_text,
        "status": query.status,
        "critique_notes": query.critique_notes,
        "research_rounds": query.research_rounds,
        "findings": [f.content for f in query.findings],
        "report": query.report.content if query.report else None,
        "created_at": query.created_at.isoformat(),
        "completed_at": query.completed_at.isoformat() if query.completed_at else None,
    }
 
