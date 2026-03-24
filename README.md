# Clinical Reconciliation Engine

A clinician-facing data reconciliation platform that resolves conflicting medication data, validates patient record quality, and presents review-ready recommendations in a clear dashboard.

Repository contents include:

- all backend and frontend source code
- runnable Docker setup
- example request payloads in `examples/`
- a brief architecture rationale in `docs/architecture-decisions.md`

## Stack

- Backend: FastAPI + Pydantic
- Frontend: React + Vite + Tailwind CSS
- AI: OpenAI API (`gpt-4.1-mini` by default) with deterministic fallback and in-memory response caching
- ML: lightweight `scikit-learn` logistic regression confidence calibration layer
- Auth: simple API key header (`x-api-key`)
- Storage: in-memory only for this version

## Features

- `POST /api/reconcile/medication`
- `POST /api/validate/data-quality`
- clinician dashboard for both workflows
- confidence scoring and safety indicator
- duplicate candidate detection for medication records with matching normalized names
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

## Deployment

The application is structured so the frontend and backend can be deployed as separate Vercel
projects:

- Frontend project root: `frontend/`
- Backend project root: `backend/`

### Vercel Deployment Notes

Frontend environment variables:

```bash
VITE_API_BASE_URL=https://your-backend-project.vercel.app
VITE_API_KEY=your-api-key
```

Backend environment variables:

```bash
API_KEY=your-api-key
OPENAI_API_KEY=your-openai-key
OPENAI_MODEL=gpt-4.1-mini
```

The backend exports the FastAPI application from `backend/app/index.py`, which is a supported
entrypoint pattern for Vercel FastAPI deployments.

## API Design

### `POST /api/reconcile/medication`

Accepts patient context and a list of conflicting medication records. The service scores each source based on:

- source reliability
- recency
- rough condition-medication fit
- disagreement across sources
- duplicate candidate detection using normalized medication-name grouping

Then it returns:

- reconciled medication
- confidence score
- reasoning
- recommended actions
- clinical safety check
- duplicate candidate groups when likely duplicate medication records are detected

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
- a lightweight logistic regression model calibrates confidence using structured reconciliation features
- the LLM is used for concise clinician-friendly explanation
- if the API key is missing or the call fails, the backend falls back to deterministic reasoning
- identical payloads are cached in memory to reduce repeat API usage and improve response efficiency

Prompt design goals:

- keep the model grounded in the provided payload only
- discourage hallucination
- request short, readable explanations suitable for a clinician review screen

## Which LLM API I Used and Why

I used the OpenAI API, with `gpt-4.1-mini` as the default model. I chose it because it is fast, affordable to operate, and strong enough for concise clinical-style reasoning and explanations. I kept the deterministic reconciliation and validation logic separate so the app remains reliable even if the model is unavailable.

## ML Extension for Future Scaling

I added a lightweight logistic regression model as a confidence calibration layer for medication reconciliation. The deterministic rules still choose the winning medication record, but the ML model looks at structured features such as reliability, recency, disagreement level, and winner margin to estimate how strong that decision is.

This confidence layer is intentionally lightweight and designed to evolve as more labeled reconciliation outcomes become available. In a production environment, the model would be retrained on real resolved cases rather than synthetic training examples.

## Key Design Decisions

- FastAPI was chosen for speed, strong validation, and clean API contracts.
- React + Vite kept the frontend lightweight and fast to iterate on.
- In-memory storage was enough for the scope because persistence was optional.
- The app uses a hybrid AI pattern rather than pure LLM output so the system stays explainable and resilient when the model is unavailable.
- A separate architecture note is included in `docs/architecture-decisions.md`.

## Key Design Decisions and Trade-offs

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

## Product Roadmap

- stronger medication parsing
- persistent storage for reconciliation decisions
- more detailed confidence calibration
- richer LLM prompts with structured JSON output
- deployment to Railway or Render plus Vercel
- a more complete audit trail for clinician review actions

## Estimated Time Spent

Estimated implementation time: approximately 5 days across backend API design,
frontend dashboard development, AI and ML integration, testing, containerization,
and documentation.
