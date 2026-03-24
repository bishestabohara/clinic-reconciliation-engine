from __future__ import annotations

from pathlib import Path
from typing import Optional

import joblib


MODEL_PATH = Path(__file__).resolve().parents[2] / "models" / "confidence_model.joblib"
_model = None


def get_confidence_model():
    global _model
    if _model is None and MODEL_PATH.exists():
        _model = joblib.load(MODEL_PATH)
    return _model


def predict_confidence(features: list[float]) -> Optional[float]:
    model = get_confidence_model()
    if model is None:
        return None

    probability = model.predict_proba([features])[0][1]
    return float(probability)
