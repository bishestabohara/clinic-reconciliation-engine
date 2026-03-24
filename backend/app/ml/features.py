from __future__ import annotations

from typing import List


def build_confidence_features(
    *,
    reliability_score: float,
    recency_score: float,
    context_bonus: float,
    winner_margin: float,
    unique_med_count: int,
    total_sources: int,
    has_pharmacy_evidence: int,
    has_portal_contradiction: int,
) -> List[float]:
    return [
        reliability_score,
        recency_score,
        context_bonus,
        winner_margin,
        float(unique_med_count),
        float(total_sources),
        float(has_pharmacy_evidence),
        float(has_portal_contradiction),
    ]
