from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.data import NUMERIC_COLUMNS, BINARY_COLUMNS


def build_model_pipeline():

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                StandardScaler(),
                NUMERIC_COLUMNS
            ),
            (
                "binary",
                "passthrough",
                BINARY_COLUMNS
            ),
        ]
    )

    model = LogisticRegression(
        class_weight="balanced",
        max_iter=1500,
        random_state=42
    )

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", model)
    ])

    return pipeline