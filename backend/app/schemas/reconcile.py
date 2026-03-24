from datetime import date
from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field


Reliability = Literal["high", "medium", "low"]


class PatientContext(BaseModel):
    age: int = Field(..., ge=0, le=120)
    conditions: list[str] = Field(default_factory=list)
    recent_labs: Dict[str, Union[float, int, str]] = Field(default_factory=dict)


class MedicationSource(BaseModel):
    system: str = Field(..., min_length=1)
    medication: str = Field(..., min_length=1)
    last_updated: Optional[date] = None
    last_filled: Optional[date] = None
    source_reliability: Reliability


class MedicationReconcileRequest(BaseModel):
    patient_context: PatientContext
    sources: list[MedicationSource] = Field(..., min_length=1)


class MedicationReconcileResponse(BaseModel):
    reconciled_medication: str
    confidence_score: float = Field(..., ge=0, le=1)
    reasoning: str
    recommended_actions: list[str]
    clinical_safety_check: str
    duplicate_candidates: List[Dict[str, Union[List[str], str]]] = Field(default_factory=list)
