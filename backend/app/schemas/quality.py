from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, Field


Severity = Literal["low", "medium", "high"]


class Demographics(BaseModel):
    name: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None


class VitalSigns(BaseModel):
    blood_pressure: Optional[str] = None
    heart_rate: Optional[int] = Field(default=None, ge=0, le=300)


class DataQualityRequest(BaseModel):
    demographics: Demographics = Field(default_factory=Demographics)
    medications: list[str] = Field(default_factory=list)
    allergies: list[str] = Field(default_factory=list)
    conditions: list[str] = Field(default_factory=list)
    vital_signs: VitalSigns = Field(default_factory=VitalSigns)
    last_updated: date


class ScoreBreakdown(BaseModel):
    completeness: int = Field(..., ge=0, le=100)
    accuracy: int = Field(..., ge=0, le=100)
    timeliness: int = Field(..., ge=0, le=100)
    clinical_plausibility: int = Field(..., ge=0, le=100)


class QualityIssue(BaseModel):
    field: str
    issue: str
    severity: Severity


class DataQualityResponse(BaseModel):
    overall_score: int = Field(..., ge=0, le=100)
    breakdown: ScoreBreakdown
    issues_detected: list[QualityIssue]
