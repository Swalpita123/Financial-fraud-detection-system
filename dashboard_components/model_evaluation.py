
from pathlib import Path
from io import BytesIO
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import streamlit as st


# =========================
# Purple theme palette
# =========================
BG_COLOR = "#09070F"
PANEL_COLOR = "#171023"
BORDER_COLOR = "#38264F"
PURPLE = "#6D28D9"
SOFT_PURPLE = "#A78BFA"
LAVENDER = "#DDD6FE"
TEXT_COLOR = "#E9DFFF"
WHITE = "#FFFFFF"


# Apply purple theme to Matplotlib figures created in this module
plt.rcParams.update({
    "figure.facecolor": BG_COLOR,
    "axes.facecolor": PANEL_COLOR,
    "axes.edgecolor": BORDER_COLOR,
    "axes.labelcolor": TEXT_COLOR,
    "axes.titlecolor": LAVENDER,
    "xtick.color": TEXT_COLOR,
    "ytick.color": TEXT_COLOR,
    "text.color": TEXT_COLOR,
    "grid.color": BORDER_COLOR,
    "legend.facecolor": PANEL_COLOR,
    "legend.edgecolor": BORDER_COLOR,
    "savefig.facecolor": BG_COLOR,
    "savefig.edgecolor": BG_COLOR,
})

def render_purple_chart(image_path: Path):
    image = Image.open(image_path).convert("RGB")
    original = np.array(image)
    pixels = original.copy()

    # Preserve the original background and chart colors.
    # Change only dark pixels that are not part of the background.
    background_mask = (
        (original[:, :, 0] < 45)
        & (original[:, :, 1] < 35)
        & (original[:, :, 2] < 60)
    )

    black_mask = (
        (original[:, :, 0] < 100)
        & (original[:, :, 1] < 100)
        & (original[:, :, 2] < 100)
        & (~background_mask)
    )

    # Make dark text white
    pixels[black_mask] = [255, 255, 255]

    recolored_image = Image.fromarray(pixels)

    buffer = BytesIO()
    recolored_image.save(buffer, format="PNG")
    buffer.seek(0)

    st.image(buffer, use_container_width=True)
    
def render_metric_card(label: str, value: float):
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(145deg, {PANEL_COLOR}, #211433);
            border: 1px solid {BORDER_COLOR};
            border-left: 4px solid {PURPLE};
            border-radius: 12px;
            padding: 16px 12px;
            min-height: 105px;
            box-shadow: 0 4px 16px rgba(109, 40, 217, 0.12);
        ">
            <div style="
                color: {SOFT_PURPLE};
                font-size: 13px;
                font-weight: 600;
                margin-bottom: 12px;
            ">{label}</div>
            <div style="
                color: {WHITE};
                font-size: 27px;
                font-weight: 700;
            ">{value:.3f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_chart_heading(caption: str):
    st.markdown(
        f"""
        <div style="
            background: {PANEL_COLOR};
            border: 1px solid {BORDER_COLOR};
            border-bottom: 2px solid {PURPLE};
            border-radius: 12px 12px 0 0;
            padding: 12px 15px;
            margin-top: 12px;
            color: {LAVENDER};
            font-weight: 600;
            font-size: 14px;
        ">{caption}</div>
        """,
        unsafe_allow_html=True,
    )


def render_model_evaluation(metrics, artifacts_dir: Path):
    st.subheader("Held-out test-set performance")

    # =========================
    # Metric cards
    # =========================
    metric_columns = st.columns(5, gap="small")

    labels = [
        "Accuracy",
        "Precision",
        "Recall",
        "F1-score",
        "Average precision",
    ]

    keys = [
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "average_precision",
    ]

    for column, label, key in zip(metric_columns, labels, keys):
        with column:
            render_metric_card(label, metrics[key])

    # =========================
    # Confusion matrix explanation
    # =========================
    st.markdown(
        f"""
        <div style="
            background: {PANEL_COLOR};
            border: 1px solid {BORDER_COLOR};
            border-radius: 10px;
            padding: 14px 16px;
            margin-top: 20px;
            margin-bottom: 18px;
            color: {TEXT_COLOR};
        ">
            <span style="color: {LAVENDER}; font-weight: 700;">
                Confusion matrix
            </span>
            <br>
            <span style="font-size: 13px;">
                Identifies correct predictions, false positives, and
                false negatives.
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =========================
    # Evaluation charts
    # =========================
    images = [
        ("confusion_matrix.png", "Confusion Matrix"),
        ("precision_recall_curve.png", "Precision-Recall Curve"),
        (
            "transaction_amount_distribution.png",
            "Transaction Amount Distribution",
        ),
        ("fraud_by_hour.png", "Fraud-Label Rate by Hour"),
        ("feature_coefficients.png", "Logistic Regression Coefficients"),
    ]

    for index in range(0, len(images), 2):
        columns = st.columns(2, gap="large")

        for column, (filename, caption) in zip(
            columns, images[index:index + 2]
        ):
            image_path = artifacts_dir / filename

            with column:
                render_chart_heading(caption)

                if image_path.exists():
                    render_purple_chart(image_path)
                else:
                    st.warning(
                        f"{filename} not found. "
                        "Run `python -m src.train` to generate it."
                    )

    # =========================
    # System architecture
    # =========================
    # architecture_path = artifacts_dir / "architecture.png"

    # if architecture_path.exists():
    #     render_chart_heading("System Architecture")
    #     render_purple_chart(architecture_path)
    # else:
    #     st.info("architecture.png not found in the artifacts folder.")
