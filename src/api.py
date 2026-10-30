from pathlib import Path

import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException

from src.schemas import (
    TransactionInput,
    TransactionPrediction,
    BatchPredictionRequest,
    BatchPredictionResponse,
)


ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "artifacts" / "fraud_model.joblib"

app = FastAPI(
    title="Financial Fraud Detection API",
    description=(
        "ML portfolio demonstration using synthetic transaction data. "
        "Not intended for real financial decisions."
    ),
    version="1.0.0"
)

_model_bundle = None


def get_model_bundle():
    global _model_bundle

    if _model_bundle is None:
        if not MODEL_PATH.exists():
            raise HTTPException(
                status_code=503,
                detail="Model not found. Run python -m src.train first."
            )

        _model_bundle = joblib.load(MODEL_PATH)

    return _model_bundle


def predict_one(transaction: TransactionInput):
    bundle = get_model_bundle()

    features = pd.DataFrame(
        [transaction.to_feature_dict()],
        columns=bundle["features"]
    )

    model = bundle["model"]

    probability = float(
        model.predict_proba(features)[0, 1]
    )

    prediction = int(probability >= 0.5)

    if probability >= 0.70:
        risk = "High"
    elif probability >= 0.35:
        risk = "Medium"
    else:
        risk = "Low"

    return TransactionPrediction(
        fraud_prediction=prediction,
        fraud_probability=round(probability, 4),
        risk_level=risk,
        disclaimer=(
            "Synthetic-data demonstration only. "
            "Do not use for real financial decisions."
        )
    )


@app.get("/")
def root():
    return {
        "message": "Financial Fraud Detection API",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_file_exists": MODEL_PATH.exists()
    }


@app.get("/model-info")
def model_info():
    bundle = get_model_bundle()
    metrics = bundle["metrics"]

    return {
        "model": metrics["model"],
        "dataset_type": metrics["dataset_type"],
        "features": bundle["features"],
        "metrics": {
            key: metrics[key]
            for key in [
                "accuracy",
                "precision",
                "recall",
                "f1_score",
                "average_precision",
                "roc_auc"
            ]
        }
    }


@app.post(
    "/predict",
    response_model=TransactionPrediction
)
def predict(transaction: TransactionInput):
    return predict_one(transaction)


@app.post(
    "/predict-batch",
    response_model=BatchPredictionResponse
)
def predict_batch(request: BatchPredictionRequest):
    predictions = [
        predict_one(transaction)
        for transaction in request.transactions
    ]

    return BatchPredictionResponse(
        predictions=predictions
    )