from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression


MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "confidence_model.joblib"


def main() -> None:
    X = np.array(
        [
            [1.0, 0.98, 0.15, 0.28, 1, 2, 0, 0],
            [1.0, 0.95, 0.15, 0.24, 2, 3, 1, 0],
            [0.75, 0.92, 0.15, 0.18, 2, 3, 1, 0],
            [1.0, 0.90, 0.00, 0.16, 2, 2, 0, 0],
            [0.75, 0.88, 0.00, 0.14, 2, 3, 1, 0],
            [0.5, 0.85, 0.00, 0.08, 3, 3, 1, 1],
            [1.0, 0.80, 0.15, 0.10, 3, 3, 0, 0],
            [0.75, 0.70, 0.00, 0.07, 3, 4, 1, 1],
            [0.5, 0.65, 0.00, 0.05, 3, 4, 1, 1],
            [1.0, 0.60, 0.15, 0.12, 2, 3, 0, 0],
            [0.5, 0.55, 0.00, 0.04, 4, 4, 1, 1],
            [0.75, 0.50, 0.00, 0.03, 4, 4, 0, 1],
            [1.0, 0.97, 0.15, 0.30, 1, 1, 0, 0],
            [1.0, 0.93, 0.15, 0.22, 1, 2, 1, 0],
            [0.75, 0.82, 0.15, 0.12, 2, 2, 0, 0],
            [0.5, 0.72, 0.00, 0.06, 3, 3, 1, 0],
            [0.5, 0.45, 0.00, 0.02, 4, 4, 1, 1],
            [1.0, 0.40, 0.00, 0.05, 3, 4, 0, 1],
            [0.75, 0.96, 0.15, 0.20, 2, 2, 1, 0],
            [0.75, 0.58, 0.00, 0.04, 3, 4, 1, 1],
        ],
        dtype=float,
    )
    y = np.array(
        [1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0],
        dtype=int,
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Saved confidence model to {MODEL_PATH}")


if __name__ == "__main__":
    main()
