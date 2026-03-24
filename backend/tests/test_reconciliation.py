from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_reconcile_medication_returns_best_candidate() -> None:
    response = client.post(
        "/api/reconcile/medication",
        headers={"x-api-key": "dev-api-key"},
        json={
            "patient_context": {
                "age": 67,
                "conditions": ["Type 2 Diabetes", "Hypertension"],
                "recent_labs": {"eGFR": 45},
            },
            "sources": [
                {
                    "system": "Hospital EHR",
                    "medication": "Metformin 1000mg twice daily",
                    "last_updated": "2024-10-15",
                    "source_reliability": "high",
                },
                {
                    "system": "Primary Care",
                    "medication": "Metformin 500mg twice daily",
                    "last_updated": "2025-01-20",
                    "source_reliability": "high",
                },
            ],
        },
    )

    assert response.status_code == 200
    assert response.json()["reconciled_medication"] == "Metformin 500mg twice daily"


def test_reconcile_conflicts_reduce_confidence() -> None:
    response = client.post(
        "/api/reconcile/medication",
        headers={"x-api-key": "dev-api-key"},
        json={
            "patient_context": {
                "age": 67,
                "conditions": ["Type 2 Diabetes"],
                "recent_labs": {"eGFR": 45},
            },
            "sources": [
                {
                    "system": "Hospital EHR",
                    "medication": "Metformin 1000mg twice daily",
                    "last_updated": "2025-01-20",
                    "source_reliability": "high",
                },
                {
                    "system": "Primary Care",
                    "medication": "Metformin 500mg twice daily",
                    "last_updated": "2025-01-19",
                    "source_reliability": "high",
                },
                {
                    "system": "Patient Portal",
                    "medication": "Not currently taking metformin",
                    "last_updated": "2025-01-18",
                    "source_reliability": "low",
                },
            ],
        },
    )

    assert response.status_code == 200
    assert response.json()["confidence_score"] < 0.9
