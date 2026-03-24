# Architecture Decisions

This document explains the main technical choices for the Clinical Reconciliation Engine.

## 1. FastAPI for the Backend

I chose FastAPI because it is fast to develop with, has strong request and response validation through Pydantic, and makes it easy to produce clean REST endpoints for a clinician-facing workflow platform. It also keeps the codebase readable by separating routes, schemas, services, and core utilities.

## 2. React + Vite for the Frontend

I chose React because it is a common and productive choice for building interactive dashboards. Vite kept the development workflow lightweight and quick, which helped me focus time on the product logic instead of frontend tooling setup.

## 3. Tailwind CSS for Rapid UI Development

Tailwind made it easy to build a clinician-friendly dashboard quickly while keeping the layout consistent. The priority was clarity and speed of iteration rather than building a custom design system upfront.

## 4. Hybrid AI Design Instead of LLM-Only Logic

The reconciliation and data quality workflows use a hybrid approach:

- deterministic scoring handles the core decision logic
- the LLM is used for concise clinical-style reasoning and summaries

I chose this approach because it is more reliable and testable than letting the model make the entire decision. It also makes it easier to explain the logic during the review interview.

## 5. OpenAI API with Fallback Behavior

The backend is wired to use the OpenAI API when `OPENAI_API_KEY` is present. If the key is missing or the model call fails, the app falls back to deterministic reasoning text so the application still works. This keeps the platform resilient and shows graceful error handling.

## 6. In-Memory Storage

I intentionally kept storage in memory for this version because it reduced setup complexity and let me prioritize reconciliation, validation, AI, and frontend workflows first.

## 7. Docker for Portability

I added Dockerfiles for the frontend and backend plus a root `docker-compose.yml` so the whole application can be started with a single command. This improves portability and supports consistent local and deployment-oriented workflows.

## 8. Test Scope

I focused test coverage on the most important backend paths:

- authentication behavior
- reconciliation result selection
- confidence handling under conflict
- data quality issue detection
- stale record handling

This gave strong coverage over the highest-risk logic without introducing a large and brittle test harness too early in the product lifecycle.
