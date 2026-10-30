import numpy as np
import pandas as pd

FEATURE_COLUMNS = [
    "amount",
    "hour",
    "distance_from_home_km",
    "distance_from_last_transaction_km",
    "ratio_to_median_purchase_price",
    "used_chip",
    "used_pin",
    "online_order",
]

NUMERIC_COLUMNS = [
    "amount",
    "hour",
    "distance_from_home_km",
    "distance_from_last_transaction_km",
    "ratio_to_median_purchase_price",
]

BINARY_COLUMNS = ["used_chip", "used_pin", "online_order"]


def generate_transactions(
    n_samples=12000,
    random_state=42
):
    rng = np.random.default_rng(random_state)

    amount = np.clip(
        rng.lognormal(3.7, 1.0, n_samples), 1, 5000
    )

    hour = rng.integers(0, 24, n_samples)

    distance_home = np.clip(
        rng.gamma(1.8, 8.0, n_samples), 0, 250
    )

    distance_last = np.clip(
        rng.gamma(1.5, 5.5, n_samples), 0, 200
    )

    purchase_ratio = np.clip(
        rng.lognormal(0, 0.8, n_samples), 0.05, 25
    )

    used_chip = rng.binomial(1, 0.58, n_samples)
    used_pin = rng.binomial(1, 0.62, n_samples)
    online_order = rng.binomial(1, 0.45, n_samples)

    # Illustrative label-generation rule.
    # These are synthetic labels, not real fraud records.
    logit = (
        -3.2
        + 0.001 * amount
        + 0.045 * distance_home
        + 0.025 * distance_last
        + 0.38 * purchase_ratio
        + 0.95 * (hour <= 4)
        + 0.8 * online_order
        - 0.85 * used_chip
        - 0.55 * used_pin
    )

    probability = 1 / (
        1 + np.exp(-np.clip(logit, -20, 20))
    )

    is_fraud = rng.binomial(1, probability)

    df = pd.DataFrame({
        "amount": amount.round(2),
        "hour": hour,
        "distance_from_home_km": distance_home.round(2),
        "distance_from_last_transaction_km": distance_last.round(2),
        "ratio_to_median_purchase_price": purchase_ratio.round(3),
        "used_chip": used_chip,
        "used_pin": used_pin,
        "online_order": online_order,
        "is_fraud": is_fraud,
    })

    return df