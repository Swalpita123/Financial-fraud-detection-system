from fastapi.testclient import TestClient

from src.api import app
from src.train import train_model


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["docs"] == "/docs"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_invalid_hour():
    response = client.post(
        "/predict",
        json={
            "amount": 100,
            "hour": 25,
            "distance_from_home_km": 1,
            "distance_from_last_transaction_km": 1,
            "ratio_to_median_purchase_price": 1,
            "used_chip": 1,
            "used_pin": 1,
            "online_order": 0
        }
    )

    assert response.status_code == 422


def test_prediction():
    train_model(n_samples=1500)

    # Clear the API's cached model so it loads the new artifact.
    import src.api as api_module
    api_module._model_bundle = None

    response = client.post(
        "/predict",
        json={
            "amount": 250,
            "hour": 2,
            "distance_from_home_km": 80,
            "distance_from_last_transaction_km": 50,
            "ratio_to_median_purchase_price": 4,
            "used_chip": 0,
            "used_pin": 0,
            "online_order": 1
        }
    )

    assert response.status_code == 200

    result = response.json()

    assert result["fraud_prediction"] in [0, 1]
    assert 0 <= result["fraud_probability"] <= 1
    assert result["risk_level"] in ["Low", "Medium", "High"]


def test_empty_batch_rejected():
    response = client.post(
        "/predict-batch",
        json={"transactions": []}
    )

    assert response.status_code == 422