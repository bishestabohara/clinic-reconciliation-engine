# Clinical Reconciliation Engine

A take-home assessment project for the Full Stack Developer - EHR Integration Intern role. The app reconciles conflicting medication data, validates patient record quality, and presents the results in a clinician-friendly dashboard.

Repository contents include:

- all backend and frontend source code
- runnable Docker setup
- example request payloads in `examples/`
- a brief architecture rationale in `docs/architecture-decisions.md`

## Stack

- Backend: FastAPI + Pydantic
- Frontend: React + Vite + Tailwind CSS
- AI: OpenAI API (`gpt-4.1-mini` by default) with deterministic fallback and in-memory response caching
- Auth: simple API key header (`x-api-key`)
- Storage: in-memory only for this version

## Features

- `POST /api/reconcile/medication`
- `POST /api/validate/data-quality`
- clinician dashboard for both workflows
- confidence scoring and safety indicator
- approve/reject UI for AI suggestions
- unit tests for reconciliation, quality checks, and auth
- Docker support with `docker-compose`

## Local Setup

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The backend runs on `http://localhost:8000`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend runs on `http://localhost:5173`.

### Environment Variables

Copy the root `.env.example` values into your local shell or a `.env` file:

```bash
API_KEY=dev-api-key
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
VITE_API_BASE_URL=http://localhost:8000
VITE_API_KEY=dev-api-key
```

### Example Payloads

Example request payloads are included here:

- `examples/reconcile-medication-request.json`
- `examples/data-quality-request.json`

## Docker

```bash
docker compose up --build
```

This starts:

- frontend on `http://localhost:5173`
- backend on `http://localhost:8000`

## API Design

### `POST /api/reconcile/medication`

Accepts patient context and a list of conflicting medication records. The service scores each source based on:

- source reliability
- recency
- rough condition-medication fit
- disagreement across sources

Then it returns:

- reconciled medication
- confidence score
- reasoning
- recommended actions
- clinical safety check

### `POST /api/validate/data-quality`

Scores a patient record across:

- completeness
- accuracy
- timeliness
- clinical plausibility

It also returns a structured issue list for the frontend to display.

## Prompt Engineering Approach

The backend uses a hybrid approach:

- deterministic rules handle scoring and guardrails
- the LLM is used for concise clinician-friendly explanation
- if the API key is missing or the call fails, the backend falls back to deterministic reasoning
- identical payloads are cached in memory to reduce repeat API usage during demos

Prompt design goals:

- keep the model grounded in the provided payload only
- discourage hallucination
- request short, readable explanations suitable for a clinician review screen

## Which LLM API I Used and Why

I used the OpenAI API, with `gpt-4.1-mini` as the default model. I chose it because it is fast, affordable for a take-home demo, and strong enough for concise clinical-style reasoning and explanations. I kept the deterministic reconciliation and validation logic separate so the app remains reliable even if the model is unavailable.

## Key Design Decisions

- FastAPI was chosen for speed, strong validation, and clean API contracts.
- React + Vite kept the frontend lightweight and fast to iterate on.
- In-memory storage was enough for the scope because persistence was optional.
- The app uses a hybrid AI pattern rather than pure LLM output so the system stays explainable and resilient when the model is unavailable.
- A separate architecture note is included in `docs/architecture-decisions.md`.

## Trade-offs

- Medication normalization is intentionally lightweight and rule-based.
- The clinical logic is not meant to replace real medication reconciliation workflows.
- Caching is in-memory only, so it resets on restart.
- Approval and rejection are UI-only in this version and are not persisted.

## Testing

```bash
cd backend
source .venv/bin/activate
pytest
```

Current verification status:

- backend tests: 6 passing
- frontend production build: passing

## What I Would Improve With More Time

- stronger medication parsing and duplicate detection
- persistent storage for reconciliation decisions
- more detailed confidence calibration
- richer LLM prompts with structured JSON output
- deployment to Railway or Render plus Vercel
- a more complete audit trail for clinician review actions

## Estimated Time Spent

Approximately 10-14 hours for scaffold, core backend logic, dashboard, tests, and containerization.
