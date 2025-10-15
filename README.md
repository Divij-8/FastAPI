# Vehicle Service Breakdown AI Knowledge Assistant

Full-stack Retrieval-Augmented Generation (RAG) assistant to help technicians diagnose and repair breakdowns by querying service manuals, diagnostic codes, and vehicle specs.

## Tech Stack
- Backend: FastAPI, LangChain, ChromaDB, OpenAI (GPT-3.5), Python 3.11
- Frontend: React 18, Vite, Tailwind CSS
- Deployment: Docker, Docker Compose

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Optional: Python 3.11 and Node 20 for local dev without Docker

### One command (Docker Compose)
```bash
./scripts/dev.sh
```
- Backend: http://localhost:8000 (Swagger at /docs)
- Frontend: http://localhost:5173 (served by nginx, proxies /api to backend)

Set `OPENAI_API_KEY` in your shell if you want LLM answers:
```bash
export OPENAI_API_KEY=sk-... # optional; offline mode uses fake embeddings
```

### Local Dev (without Docker)
Backend:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn app.main:app --reload --app-dir backend
```
Frontend:
```bash
cd frontend
npm i
npm run dev
```
Set `VITE_API_BASE_URL=http://localhost:8000` in `frontend/.env` for local dev.

## API Endpoints
- GET `/health`
- POST `/upload-documents` (multipart PDFs)
- POST `/query` (body: `{ query, top_k, vehicle? }`)
- GET `/diagnostic-codes/{code}`
- GET `/vehicle-info/{make}/{model}/{year}`

### Example Requests
```bash
# Health
curl http://localhost:8000/health

# Upload PDFs
curl -X POST http://localhost:8000/upload-documents \
  -F files=@/path/to/manual.pdf

# Query
curl -X POST http://localhost:8000/query \
  -H 'Content-Type: application/json' \
  -d '{"query":"P0300 misfire diagnosis for 2018 Toyota Camry","top_k":3,"vehicle":{"make":"Toyota","model":"Camry","year":2018}}'

# Diagnostic code
curl http://localhost:8000/diagnostic-codes/P0300

# Vehicle info
curl http://localhost:8000/vehicle-info/Toyota/Camry/2018
```

## Frontend UI
- Chat interface with source citations and loading/error states
- PDF upload panel
- Vehicle context form (sets context and fetches specs)
- Diagnostic code lookup

## Testing
```bash
./scripts/test.sh
```
- Backend: pytest
- Frontend: Vitest + React Testing Library (skips if npm missing)

## Project Structure
```
backend/
  app/
    routers/, services/, models.py, config.py, main.py
  data/ diagnostic_codes.json, vehicle_specs.json
  tests/
frontend/
  src/components, context, tests, vite config
scripts/
```

## Environment Variables
- Backend: see `backend/.env.example`
- Frontend: optional `frontend/.env` with `VITE_API_BASE_URL`

## Hackathon 24-hour Timeline (MVP-first)
- Hour 0-2: Scope, data, API spec, scaffold backend/frontend
- Hour 2-6: Backend ingestion + Chroma + RAG path, health/data endpoints
- Hour 6-10: Query endpoint prompt engineering, sources wiring
- Hour 10-14: Frontend chat + upload + vehicle forms
- Hour 14-18: Dockerfiles + compose + local scripts
- Hour 18-20: Tests (backend + frontend), sample data
- Hour 20-22: Polish UX, error states, loading skeletons
- Hour 22-24: README, demo prep, run-through

## Presentation Outline
- Problem and technician pain points
- Solution demo: upload, ask, cite sources
- Architecture: FastAPI + LangChain + Chroma + React
- Data handling: PDFs, chunks, metadata
- RAG flow and prompt design
- Limitations and next steps (multi-make models, richer tools, telemetry)
- Live Q&A
