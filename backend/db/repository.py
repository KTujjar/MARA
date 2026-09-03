from datetime import datetime, timezone, UTC

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Finding, Query, Report

def create_query(db: Session, query_text: str) -> Query:
    query = Query(query_text=query_text, status="running")
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def add_finding(db: Session, query_id: int, round_number: int, content: str) -> Finding:
    
    finding = Finding(query_id=query_id, round_number=round_number, content=content)
    db.add(finding)
    db.commit()
    return finding

def set_critique_notes(db: Session, query_id: int, notes: str, research_rounds: int) -> None:
    query = db.get(Query, query_id)
    if query is None:
        return
    query.critique_notes = notes
    query.research_rounds = research_rounds
    db.commit()

def save_report(db: Session, query_id: int, content: str) -> Report:
    report = Report(query_id=query_id, content=content)
    db.add(report)
    
    query = db.get(Query, query_id)
    if query is not None:
        query.status = "done"
        query.completed_at = datetime.now(UTC)

    db.commit()
    db.refresh(report)
    return report

def mark_failed(db: Session, query_id: int, error_message: str) -> None:
    query = db.get(Query, query_id)
    if query is None:
        return
    query.status = "error"
    query.critique_notes = (query.critique_notes or "") + f"\n[error] {error_message}"
    db.commit()

def list_history(db: Session, limit: int = 20) -> list[Query]:
    stmt = select(Query).order_by(Query.created_at.desc()).limit(limit)
    return list(db.scalars(stmt))

def get_query_with_report(db: Session, query_id: int) -> Query | None:
    return db.get(Query, query_id)
