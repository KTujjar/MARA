"""SQLAlchemy models for persisting research queries, findings, and reports.
 
Three tables, matching the shape of ResearchState in graph/state.py:
  - Query:   one row per user question, tracks lifecycle status
  - Finding: one row per research finding (there can be several per query,
             one or more per research round)
  - Report:  the final synthesized report, one-to-one with a Query
"""

from datetime import date, datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, null
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, query, relationship

class Base(DeclarativeBase):
    pass

def _utcnow()->datetime:
    return datetime.now(timezone.utc)

class Query(Base):
    __tablename__ = "queries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    query_text: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="running", nullable=False)
    critique_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    research_rounds: Mapped[int] = mapped_column(Integer, default = 0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone = True), default = _utcnow, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone = True), nullable=True)

    findings: Mapped[list["Finding"]] = relationship(
        back_populates="query", cascade= "all, delete-orphan", order_by="Finding.id"
    )

    report: Mapped["Report | None"] = relationship(
        back_populates="query", uselist=False, cascade="all, delete-orphan"
    )

class Finding(Base):
    __tablename__ = "findings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    query_id: Mapped[int] = mapped_column(ForeignKey("queries.id"), nullable=False)
    round_number: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow, nullable=False)

    query: Mapped["Query"] = relationship(back_populates="findings")


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    query_id: Mapped[int] = mapped_column(ForeignKey("queries.id"), unique=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow, nullable=False)

    query: Mapped["Query"] = relationship(back_populates="report")

