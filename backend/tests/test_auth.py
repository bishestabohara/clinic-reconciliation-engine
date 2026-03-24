from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_missing_api_key_is_rejected() -> None:
    response = client.post(
        "/api/reconcile/medication",
        json={
            "patient_context": {"age": 40, "conditions": [], "recent_labs": {}},
            "sources": [
                {
                    "system": "Clinic",
                    "medication": "Lisinopril 10mg daily",
                    "last_updated": "2025-01-01",
                    "source_reliability": "high",
                }
            ],
        },
    )

    assert response.status_code == 401
