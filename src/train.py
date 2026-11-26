from __future__ import annotations

from datetime import datetime, timezone
import json
import uuid

import joblib
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.multioutput import MultiOutputRegressor
from sklearn.pipeline import Pipeline

from src.config import ARTIFACT_DIR, CSV_PATH, FEATURE_SCHEMA_VERSION, MODEL_PATH, REGISTRY_PATH
from src.features import build_preprocessor, split_xy
from src.metrics import evaluate_matrix
from src.split import perturbation_holdout


def train() -> dict:
    df = pd.read_csv(CSV_PATH)
    train_df, test_df, holdout = perturbation_holdout(df)

    x_train, y_train = split_xy(train_df)
    x_test, y_test = split_xy(test_df)

    model = Pipeline([
        ("preprocess", build_preprocessor()),
        ("model", MultiOutputRegressor(Ridge(alpha=1.0))),
    ])
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    metrics = evaluate_matrix(y_test.to_numpy(), pred)

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    registry = {
        "experiment_id": str(uuid.uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "model_type": "one-hot + multi-output ridge",
        "feature_schema_version": FEATURE_SCHEMA_VERSION,
        "train_rows": len(train_df),
        "test_rows": len(test_df),
        "holdout_perturbations": holdout,
        "metrics": metrics,
        "artifact": MODEL_PATH.name,
        "training_reference": {
            "dose_mean": float(train_df["dose"].mean()),
            "dose_std": float(train_df["dose"].std()),
        },
    }
    REGISTRY_PATH.write_text(json.dumps(registry, indent=2))
    return registry


if __name__ == "__main__":
    print(json.dumps(train(), indent=2))
