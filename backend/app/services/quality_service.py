from __future__ import annotations

from datetime import date

from app.schemas.quality import (
    DataQualityRequest,
    DataQualityResponse,
    QualityIssue,
    ScoreBreakdown,
)
from app.services.llm_service import generate_quality_summary


def _parse_blood_pressure(bp_value: str | None) -> tuple[int, int] | None:
    if not bp_value or "/" not in bp_value:
        return None

    systolic_raw, diastolic_raw = bp_value.split("/", maxsplit=1)
    if not systolic_raw.isdigit() or not diastolic_raw.isdigit():
        return None

    return int(systolic_raw), int(diastolic_raw)


def validate_data_quality(payload: DataQualityRequest) -> DataQualityResponse:
    issues: list[QualityIssue] = []
    completeness = 100
    accuracy = 100
    timeliness = 100
    clinical_plausibility = 100

    if not payload.allergies:
        completeness -= 20
        issues.append(
            QualityIssue(
                field="allergies",
                issue="No allergies documented - likely incomplete.",
                severity="medium",
            )
        )

    if not payload.demographics.name or not payload.demographics.dob:
        completeness -= 20
        issues.append(
            QualityIssue(
                field="demographics",
                issue="Key demographic fields are missing.",
                severity="medium",
            )
        )

    bp = _parse_blood_pressure(payload.vital_signs.blood_pressure)
    if bp and (bp[0] > 300 or bp[1] > 180):
        accuracy -= 30
        clinical_plausibility -= 45
        issues.append(
            QualityIssue(
                field="vital_signs.blood_pressure",
                issue="Blood pressure appears physiologically implausible.",
                severity="high",
            )
        )

    age_days = (date.today() - payload.last_updated).days
    if age_days > 180:
        timeliness -= 30
        issues.append(
            QualityIssue(
                field="last_updated",
                issue="Record is more than 6 months old and may be stale.",
                severity="medium",
            )
        )

    if payload.conditions and not payload.medications:
        completeness -= 20
        clinical_plausibility -= 15
        issues.append(
            QualityIssue(
                field="medications",
                issue="Conditions are documented but the medication list is empty.",
                severity="medium",
            )
        )

    breakdown = ScoreBreakdown(
        completeness=max(0, completeness),
        accuracy=max(0, accuracy),
        timeliness=max(0, timeliness),
        clinical_plausibility=max(0, clinical_plausibility),
    )
    overall_score = round(
        (
            breakdown.completeness
            + breakdown.accuracy
            + breakdown.timeliness
            + breakdown.clinical_plausibility
        )
        / 4
    )
    summary = generate_quality_summary(payload.model_dump(mode="json"), len(issues))

    return DataQualityResponse(
        overall_score=overall_score,
        breakdown=breakdown,
        issues_detected=[
            *issues,
            QualityIssue(
                field="summary",
                issue=summary,
                severity="low",
            ),
        ]
        if summary
        else issues,
    )
