from __future__ import annotations

from datetime import date

from app.schemas.reconcile import (
    MedicationReconcileRequest,
    MedicationReconcileResponse,
    MedicationSource,
)
from app.services.llm_service import generate_reconciliation_reasoning


RELIABILITY_SCORES = {"high": 1.0, "medium": 0.75, "low": 0.5}


def _source_date(source: MedicationSource) -> date:
    return source.last_updated or source.last_filled or date.min


def _condition_context_bonus(medication: str, conditions: list[str]) -> float:
    normalized_medication = medication.lower()
    condition_blob = " ".join(conditions).lower()

    if "metformin" in normalized_medication and "diabetes" in condition_blob:
        return 0.15
    if "lisinopril" in normalized_medication and "hypertension" in condition_blob:
        return 0.15
    return 0.0


def reconcile_medications(payload: MedicationReconcileRequest) -> MedicationReconcileResponse:
    ranked_sources = sorted(payload.sources, key=_source_date, reverse=True)
    newest_date = _source_date(ranked_sources[0])

    scored_sources: list[tuple[float, MedicationSource]] = []
    for source in ranked_sources:
        recency_delta = (newest_date - _source_date(source)).days if newest_date != date.min else 0
        recency_score = max(0.1, 1 - (recency_delta / 365))
        reliability_score = RELIABILITY_SCORES[source.source_reliability]
        context_bonus = _condition_context_bonus(
            medication=source.medication,
            conditions=payload.patient_context.conditions,
        )
        total_score = (0.55 * reliability_score) + (0.3 * recency_score) + context_bonus
        scored_sources.append((round(total_score, 4), source))

    best_score, best_source = max(scored_sources, key=lambda item: item[0])
    disagreement_penalty = 0.08 * max(0, len({source.medication for source in payload.sources}) - 1)
    confidence_score = max(0.35, min(0.99, round(best_score - disagreement_penalty, 2)))
    safety_check = "PASSED" if confidence_score >= 0.8 else "REVIEW"

    if any("not currently taking" in source.medication.lower() for source in payload.sources):
        safety_check = "REVIEW"

    fallback_reasoning = (
        f"{best_source.system} was selected because it offered the strongest blend of "
        f"source reliability, record recency, and fit with the patient's known conditions."
    )
    reasoning = generate_reconciliation_reasoning(payload.model_dump(mode="json"), fallback_reasoning)

    return MedicationReconcileResponse(
        reconciled_medication=best_source.medication,
        confidence_score=confidence_score,
        reasoning=reasoning,
        recommended_actions=[
            f"Confirm the active medication list with {best_source.system}.",
            "Review conflicting sources before finalizing the chart update.",
            "Document clinician approval or rejection in the reconciliation dashboard.",
        ],
        clinical_safety_check=safety_check,
    )
