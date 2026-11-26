from __future__ import annotations

import json

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.config import MODEL_PATH, REGISTRY_PATH
from src.monitoring import drift_status, standardized_mean_shift

app = FastAPI(title="Cell Perturbation ML Platform", version="0.1.0")


class PredictionRequest(BaseModel):
    perturbation: str
    cell_type: str
    dose: float = Field(gt=0, le=2)
    batch: str


class DriftRequest(BaseModel):
    mean_dose: float


def _registry() -> dict:
    if not REGISTRY_PATH.exists():
        raise HTTPException(status_code=503, detail="model registry unavailable")
    return json.loads(REGISTRY_PATH.read_text())


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/experiments")
def experiments():
    return _registry()


@app.post("/predict")
def predict(request: PredictionRequest):
    if not MODEL_PATH.exists():
        raise HTTPException(status_code=503, detail="model artifact unavailable")
    registry = _registry()
    model = joblib.load(MODEL_PATH)
    pred = model.predict(pd.DataFrame([request.model_dump()]))[0]
    return {
        "experiment_id": registry["experiment_id"],
        "feature_schema_version": registry["feature_schema_version"],
        "predicted_expression": {f"gene_{i:03d}": float(v) for i, v in enumerate(pred)},
    }


@app.post("/monitor/drift")
def monitor_drift(request: DriftRequest):
    ref = _registry()["training_reference"]
    shift = standardized_mean_shift(request.mean_dose, ref["dose_mean"], ref["dose_std"])
    return {"standardized_mean_shift": shift, "status": drift_status(shift)}
