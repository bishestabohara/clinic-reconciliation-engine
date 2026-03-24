from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.quality import router as quality_router
from app.api.routes.reconcile import router as reconcile_router


app = FastAPI(
    title="Clinical Reconciliation Engine",
    description="Mini clinical data reconciliation engine for internship take-home assessment.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(reconcile_router)
app.include_router(quality_router)
