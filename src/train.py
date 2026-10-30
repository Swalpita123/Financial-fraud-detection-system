from pathlib import Path
import json

import joblib
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    average_precision_score,
    roc_auc_score,
    confusion_matrix,
    precision_recall_curve,
    classification_report,
)

from src.data import FEATURE_COLUMNS, generate_transactions
from src.features import build_model_pipeline


def apply_purple_theme(ax, fig, title):
    background = "#09070F"
    panel = "#171023"
    lavender = "#A78BFA"
    white = "#FFFFFF"
    grid = "#49336B"

    fig.patch.set_facecolor(background)
    ax.set_facecolor(panel)

    ax.set_title(title, color=white, fontsize=15, pad=14)
    ax.xaxis.label.set_color(white)
    ax.yaxis.label.set_color(white)
    ax.tick_params(colors=white, labelsize=9)

    ax.grid(
        True,
        axis="y",
        color=grid,
        linewidth=0.8,
        alpha=0.8,
    )
    ax.set_axisbelow(True)

    for spine in ax.spines.values():
        spine.set_color(lavender)

    return "#7C3AED"


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
ARTIFACT_DIR = ROOT / "artifacts"



def save_confusion_matrix(y_true, y_pred):
    matrix = confusion_matrix(y_true, y_pred, labels=[0, 1])

    fig, ax = plt.subplots(figsize=(7, 5))

    sns.heatmap(
    matrix,
    annot=True,
    fmt="d",
    cmap=sns.color_palette(
        ["#171023", "#38205C", "#7C3AED", "#A78BFA"],
        as_cmap=True,
    ),
    xticklabels=["Normal", "Fraud"],
    yticklabels=["Normal", "Fraud"],
    linewidths=1,
    linecolor="#49336B",
    annot_kws={"color": "white", "fontsize": 13},
    ax=ax,
)
    
    # Make colorbar numbers white
    colorbar = ax.collections[0].colorbar
    colorbar.ax.tick_params(colors="white", labelsize=10)
    colorbar.outline.set_edgecolor("#A78BFA")

    ax.set_xlabel("Predicted label")
    ax.set_ylabel("Actual label")
    apply_purple_theme(ax, fig, "Confusion Matrix")
    ax.grid(False)

    fig.tight_layout()
    fig.savefig(
        ARTIFACT_DIR / "confusion_matrix.png",
        dpi=180,
        facecolor=fig.get_facecolor(),
        bbox_inches="tight",
    )
    plt.close(fig)



def save_precision_recall_curve(y_true, probabilities):
    precision, recall, _ = precision_recall_curve(
        y_true, probabilities
    )
    ap = average_precision_score(y_true, probabilities)

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.plot(
        recall,
        precision,
        color="#A78BFA",
        linewidth=2.5,
        label=f"Average precision = {ap:.3f}",
    )

    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.05)

    apply_purple_theme(ax, fig, "Precision-Recall Curve")
    ax.grid(True, color="#49336B", alpha=0.8)
    ax.legend(
        facecolor="#231433",
        edgecolor="#49336B",
        labelcolor="white",
    )

    fig.tight_layout()
    fig.savefig(
        ARTIFACT_DIR / "precision_recall_curve.png",
        dpi=180,
        facecolor=fig.get_facecolor(),
        bbox_inches="tight",
    )
    plt.close(fig)


def save_amount_distribution(df):
    fig, ax = plt.subplots(figsize=(8, 5))

    sns.histplot(
        data=df,
        x="amount",
        hue="is_fraud",
        bins=40,
        element="step",
        stat="count",
        common_norm=False,
        palette={0: "#7C3AED", 1: "#E9D5FF"},
        ax=ax,
    )

    ax.set_xlabel("Transaction amount")
    ax.set_ylabel("Number of transactions")

    apply_purple_theme(
        ax, fig, "Transaction Amount Distribution"
    )

    legend = ax.get_legend()
    if legend:
        legend.set_title("Fraud label")
        legend.get_title().set_color("white")
        for text_item in legend.get_texts():
            text_item.set_color("white")
        legend.get_frame().set_facecolor("#231433")
        legend.get_frame().set_edgecolor("#49336B")

    fig.tight_layout()
    fig.savefig(
        ARTIFACT_DIR / "transaction_amount_distribution.png",
        dpi=180,
        facecolor=fig.get_facecolor(),
        bbox_inches="tight",
    )
    plt.close(fig)


def save_fraud_by_hour(df):
    # Calculate fraud-label rate by hour
    hourly_fraud = (
        df.groupby("hour")["is_fraud"]
        .mean()
        .reindex(range(24), fill_value=0)
    )

    # Match the figure size used by your other charts
    fig, ax = plt.subplots(figsize=(8, 5))

    apply_purple_theme(
        ax,
        fig,
        "Fraud-Label Rate by Hour",
    )

    ax.bar(
        hourly_fraud.index,
        hourly_fraud.values,
        color="#7C3AED",
        edgecolor="#A78BFA",
        linewidth=0.4,
        width=0.75,
    )

    ax.set_xlabel("Hour of day")
    ax.set_ylabel("Fraction labelled fraud")
    ax.set_xticks(range(24))
    ax.set_xlim(-0.5, 23.5)
    ax.set_ylim(bottom=0)

    fig.tight_layout()

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = ARTIFACT_DIR / "fraud_by_hour.png"

    fig.savefig(
        output_path,
        dpi=180,
        facecolor=fig.get_facecolor(),
        bbox_inches="tight",
    )

    plt.close(fig)


def save_feature_coefficients(model):
    classifier = model.named_steps["classifier"]

    coefficients = pd.DataFrame({
        "feature": FEATURE_COLUMNS,
        "coefficient": classifier.coef_[0],
    }).sort_values("coefficient")

    fig, ax = plt.subplots(figsize=(8, 5))

    colors = [
        "#A78BFA" if value >= 0 else "#7C3AED"
        for value in coefficients["coefficient"]
    ]

    ax.barh(
        coefficients["feature"],
        coefficients["coefficient"],
        color=colors,
        edgecolor="#DDD6FE",
        linewidth=0.4,
    )

    ax.axvline(0, color="white", linewidth=0.9)
    ax.set_xlabel("Coefficient")

    apply_purple_theme(
        ax, fig, "Logistic Regression Coefficients"
    )
    ax.grid(False)
    ax.grid(axis="x", color="#49336B", alpha=0.8)

    fig.tight_layout()
    fig.savefig(
        ARTIFACT_DIR / "feature_coefficients.png",
        dpi=180,
        facecolor=fig.get_facecolor(),
        bbox_inches="tight",
    )
    plt.close(fig)

    coefficients.to_csv(
        ARTIFACT_DIR / "feature_coefficients.csv",
        index=False,
    )



def save_architecture_diagram():
    stages = [
        "Transaction Data",
        "Pandas + NumPy",
        "scikit-learn",
        "Model + Metrics",
        "FastAPI",
        "Streamlit",
    ]

    fig, ax = plt.subplots(figsize=(13, 3.5))
    fig.patch.set_facecolor("#09070F")
    ax.set_facecolor("#09070F")
    ax.axis("off")

    x_positions = np.linspace(0.08, 0.92, len(stages))

    for i, (x, stage) in enumerate(zip(x_positions, stages)):
        ax.text(
            x, 0.55, stage,
            ha="center",
            va="center",
            color="#FFFFFF",
            fontsize=10,
            bbox={
                "boxstyle": "round,pad=0.65",
                "facecolor": "#231433",
                "edgecolor": "#A78BFA",
                "linewidth": 1.3,
            },
        )

        if i < len(stages) - 1:
            ax.annotate(
                "",
                xy=(x_positions[i + 1] - 0.055, 0.55),
                xytext=(x + 0.055, 0.55),
                arrowprops={
                    "arrowstyle": "->",
                    "color": "#A78BFA",
                    "linewidth": 1.5,
                },
            )

    ax.set_title(
        "Financial Fraud Detection Architecture",
        color="#FFFFFF",
        fontsize=15,
        pad=18,
    )

    fig.tight_layout()
    fig.savefig(
        ARTIFACT_DIR / "architecture.png",
        dpi=180,
        facecolor=fig.get_facecolor(),
        bbox_inches="tight",
    )
    plt.close(fig)


def train_model(n_samples=12000):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Generate and save data
    df = generate_transactions(n_samples=n_samples)

    df.to_csv(
        DATA_DIR / "transactions.csv",
        index=False
    )

    X = df[FEATURE_COLUMNS]
    y = df["is_fraud"]

    # 2. Split into training and testing data
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # 3. Train the model
    model = build_model_pipeline()
    model.fit(X_train, y_train)

    # 4. Predict on unseen test rows
    y_pred = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    # 5. Evaluate
    metrics = {
        "dataset_type": "synthetic",
        "n_samples": int(len(df)),
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "fraud_rate": float(y.mean()),
        "accuracy": float(
            accuracy_score(y_test, y_pred)
        ),
        "precision": float(
            precision_score(
                y_test, y_pred, zero_division=0
            )
        ),
        "recall": float(
            recall_score(
                y_test, y_pred, zero_division=0
            )
        ),
        "f1_score": float(
            f1_score(
                y_test, y_pred, zero_division=0
            )
        ),
        "average_precision": float(
            average_precision_score(
                y_test, probabilities
            )
        ),
        "roc_auc": float(
            roc_auc_score(y_test, probabilities)
        ),
        "classification_report": classification_report(
            y_test,
            y_pred,
            output_dict=True,
            zero_division=0
        ),
        "features": FEATURE_COLUMNS,
        "model": "Logistic Regression"
    }

    # 6. Save model and metrics
    joblib.dump(
        {
            "model": model,
            "features": FEATURE_COLUMNS,
            "metrics": metrics
        },
        ARTIFACT_DIR / "fraud_model.joblib"
    )

    with open(
        ARTIFACT_DIR / "metrics.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(metrics, file, indent=2)

    # 7. Generate all visualizations
    save_confusion_matrix(y_test, y_pred)
    save_precision_recall_curve(y_test, probabilities)
    save_amount_distribution(df)
    save_fraud_by_hour(df)
    save_feature_coefficients(model)
    save_architecture_diagram()

    print("\nTraining complete.")
    print("Dataset: synthetic")
    print(f"Transactions: {len(df)}")
    print(f"Accuracy: {metrics['accuracy']:.3f}")
    print(f"Precision: {metrics['precision']:.3f}")
    print(f"Recall: {metrics['recall']:.3f}")
    print(f"F1-score: {metrics['f1_score']:.3f}")
    print(f"Average precision: {metrics['average_precision']:.3f}")
    print(f"ROC-AUC: {metrics['roc_auc']:.3f}")
    print(f"Artifacts saved to: {ARTIFACT_DIR}")

    return metrics


if __name__ == "__main__":
    train_model()