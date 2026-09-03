# Mara — Multi-Agent Research Assistant

A research assistant that takes a user query, plans the research, gathers information
from the web and local documents, fact-checks its own findings, and writes a synthesized
report — using multiple cooperating Claude agents (via [LangGraph](https://github.com/langchain-ai/langgraph))
rather than a single prompt-response loop.

## How it works

```
User query (React chat UI)
        |
        v
Orchestrator agent (LangGraph state machine)
        |
   -----------------------
   |                     |
   v                     v
Research agent      Critique agent
(web search + RAG)  (verifies & fact-checks)
   |                     |
   -----------------------
        |
        v
Writer agent (synthesizes final answer)
        |
        v
Final report (Markdown)
```

- **Orchestrator** — breaks the query into a short research plan.
- **Research** — searches the web (Exa) and a local document store (Chroma/RAG),
  using Claude's tool-calling to decide which to use.
- **Critique** — checks the research findings against the original question and can
  loop the graph back to Research if evidence is weak (capped to avoid infinite loops).
- **Writer** — synthesizes everything into a final Markdown report.

Every query, its findings, and its final report are persisted to SQLite, browsable
later from the frontend's History tab. Every agent run traces to LangSmith with full
prompt/completion visibility, not just which node ran.

## Tech stack

| Layer | Choice |
|---|---|
| Orchestration | LangGraph |
| LLM | Claude (Anthropic API, direct SDK — no LangChain model wrapper) |
| Retrieval (RAG) | Chroma (embedded, via LangChain) |
| Web search | Exa |
| Backend | Python + FastAPI, streamed via SSE |
| Frontend | React + TypeScript (Vite) |
| Persistence | SQLite + SQLAlchemy |
| Observability | LangSmith |
| Containerization | Docker + Docker Compose (local only — no cloud deploy configured) |

## Project structure

```
Mara/
├── .env.example
├── backend/
│   ├── agents/        # orchestrator, research, critique, writer
│   ├── graph/          # LangGraph state + graph wiring
│   ├── rag/            # Chroma ingestion + retrieval
│   ├── tools/          # web_search (Exa), local_search
│   ├── db/             # SQLAlchemy models, session, repository
│   ├── api/            # FastAPI routes (/query, /history, /reports/{id})
│   └── tests/
├── frontend/
│   └── src/
│       ├── components/ # ChatInput, StreamingAnswerPanel, AgentActivitySidebar,
│       │                # HistoryPanel, ReportView
│       ├── hooks/       # useAgentStream (SSE client)
│       └── api/         # client.ts
└── deploy/
    ├── Dockerfile.backend
    ├── Dockerfile.frontend
    └── docker-compose.yml
```

## Getting started

### Prerequisites
- Python 3.12+ and [uv](https://docs.astral.sh/uv/)
- Node 22+ and npm
- Docker Desktop (only needed for the containerized workflow)
- API keys: Anthropic, Exa, and LangSmith

### 1. Configure environment
Copy `.env.example` to `.env` at the project root and fill in real values:
```bash
cp .env.example .env
```

### 2. Run the backend
```bash
cd backend
uv sync
uv run uvicorn main:app --reload
```
Runs on `http://localhost:8000`.

### 3. Run the frontend
```bash
cd frontend
npm install
npm run dev
```
Runs on `http://localhost:5173`.

### Or: run both in Docker
```bash
cd deploy
docker compose up --build
```
SQLite and the Chroma index persist on your host disk via volume mounts, so data
survives `docker compose down` / `up` cycles.

## Environment variables

| Variable | Required | Purpose |
|---|---|---|
| `ANTHROPIC_API_KEY` | Yes | Powers all four agents |
| `EXA_API_KEY` | Yes | Web search tool |
| `LANGSMITH_TRACING` | Yes | Set to `true` to enable tracing |
| `LANGSMITH_API_KEY` | Yes | LangSmith auth |
| `LANGSMITH_PROJECT` | Yes | Groups traces in the LangSmith dashboard |
| `DATABASE_URL` | No | Defaults to `sqlite:///./db/app.db` |

## API

| Endpoint | Description |
|---|---|
| `POST /query` | Streams agent progress via SSE as the graph runs |
| `GET /history` | Lists past queries |
| `GET /reports/{id}` | Full record for one past query: findings, critique notes, report |

## Known limitations
- No cloud deploy target is configured — the Docker setup is for local development
  only. SQLite doesn't suit a stateless/serverless deploy target without further work
  (e.g. migrating to Postgres or attaching persistent storage).
- `anthropic` is pinned below `1.0.0` — `langsmith`'s `wrap_anthropic` doesn't yet
  support the Anthropic SDK's v1.0 removal of the legacy Completions API. Safe to
  re-evaluate once `langsmith` ships a compatible release.

## Project status
See [`PROJECT_STATUS.md`](./PROJECT_STATUS.md) for phase-by-phase build status.
