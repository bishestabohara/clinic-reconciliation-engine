from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_validate_quality_flags_implausible_blood_pressure() -> None:
    response = client.post(
        "/api/validate/data-quality",
        headers={"x-api-key": "dev-api-key"},
        json={
            "demographics": {"name": "John Doe", "dob": "1955-03-15", "gender": "M"},
            "medications": ["Metformin 500mg"],
            "allergies": [],
            "conditions": ["Type 2 Diabetes"],
            "vital_signs": {"blood_pressure": "340/180", "heart_rate": 72},
            "last_updated": "2024-06-15",
        },
    )

    assert response.status_code == 200
    issues = response.json()["issues_detected"]
    assert any(issue["field"] == "vital_signs.blood_pressure" for issue in issues)


def test_validate_quality_penalizes_stale_record() -> None:
    response = client.post(
        "/api/validate/data-quality",
        headers={"x-api-key": "dev-api-key"},
        json={
            "demographics": {"name": "John Doe", "dob": "1955-03-15", "gender": "M"},
            "medications": ["Metformin 500mg"],
            "allergies": ["Penicillin"],
            "conditions": ["Type 2 Diabetes"],
            "vital_signs": {"blood_pressure": "130/80", "heart_rate": 72},
            "last_updated": "2024-06-15",
        },
    )

    assert response.status_code == 200
    assert response.json()["breakdown"]["timeliness"] < 100


def test_validate_quality_flags_missing_medications_when_conditions_exist() -> None:
    response = client.post(
        "/api/validate/data-quality",
        headers={"x-api-key": "dev-api-key"},
        json={
            "demographics": {"name": "John Doe", "dob": "1955-03-15", "gender": "M"},
            "medications": [],
            "allergies": ["Penicillin"],
            "conditions": ["Type 2 Diabetes"],
            "vital_signs": {"blood_pressure": "130/80", "heart_rate": 72},
            "last_updated": "2026-03-20",
        },
    )

    assert response.status_code == 200
    issues = response.json()["issues_detected"]
    assert any(issue["field"] == "medications" for issue in issues)
