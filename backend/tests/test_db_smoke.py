"""Smoke test for the db layer — exercises repository.py against a real
SQLite file with no LangGraph/LLM calls involved. Run with:

    cd backend
    uv run python tests/test_db_smoke.py
"""
from db import repository
from db.session import SessionLocal, init_db


def main() -> None:
    init_db()  # creates the tables if they don't exist

    with SessionLocal() as db:
        query = repository.create_query(db, "What is LangGraph?")
        print("created:", query.id, query.status)

        repository.add_finding(
            db, query.id, round_number=1,
            content="LangGraph is a graph-based agent framework.",
        )
        repository.add_finding(
            db, query.id, round_number=1,
            content="It's built by the LangChain team.",
        )

        repository.set_critique_notes(
            db, query.id, notes="Looks sufficient", research_rounds=1
        )

        repository.save_report(db, query.id, content="# Report\n\nLangGraph is...")

        fetched = repository.get_query_with_report(db, query.id)
        assert fetched is not None, "query should exist right after creating it"
        assert fetched.report is not None, "report should exist right after saving it"

        print("status:", fetched.status)
        print("findings:", [f.content for f in fetched.findings])
        print("report:", fetched.report.content)
        print("history:", [(q.id, q.status) for q in repository.list_history(db)])


if __name__ == "__main__":
    main()
