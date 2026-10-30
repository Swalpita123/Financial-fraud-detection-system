from pathlib import Path
import json
import joblib
import pandas as pd
import streamlit as st

# from dashboard_components.styles import apply_dashboard_styles, render_header
from dashboard_components.styles import (
    apply_dashboard_styles,
    # render_header,
    render_sidebar
)
from dashboard_components.overview import render_overview
from dashboard_components.model_evaluation import render_model_evaluation
from dashboard_components.predictions import render_predictions
from dashboard_components.data_explorer import render_data_explorer
from dashboard_components.batch_prediction import render_batch_prediction
from src.data import FEATURE_COLUMNS

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "transactions.csv"
MODEL_PATH = ROOT / "artifacts" / "fraud_model.joblib"
METRICS_PATH = ROOT / "artifacts" / "metrics.json"
ARTIFACTS = ROOT / "artifacts"


st.set_page_config(
    page_title="Fraud Intelligence",
    page_icon="🛡️",
    layout="wide",
)

apply_dashboard_styles()
# render_header()

if not (DATA_PATH.exists() and MODEL_PATH.exists() and METRICS_PATH.exists()):
    st.warning(
        "Project artifacts are missing. Run "
        "`python -m src.train` from your project root first."
    )
    st.stop()


@st.cache_data
def load_data(path, modified_time):
    return pd.read_csv(path)


@st.cache_data
def load_metrics(path, modified_time):
    with open(path, encoding="utf-8") as file:
        return json.load(file)


df = load_data(str(DATA_PATH), DATA_PATH.stat().st_mtime)
metrics = load_metrics(str(METRICS_PATH), METRICS_PATH.stat().st_mtime)
bundle = joblib.load(MODEL_PATH)
model = bundle["model"]




total = len(df)
fraud_count = int(df["is_fraud"].sum())
fraud_rate = df["is_fraud"].mean() * 100

selected_page = render_sidebar(total, fraud_rate)

# st.divider()

if selected_page == "📊 Analytics":
    
    st.markdown(
        '<div style="height: 20px;"></div>',
        unsafe_allow_html=True
    )

    # Metrics displayed ONLY on Analytics page
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Transactions analyzed", f"{total:,}")
    c2.metric("Fraud-labelled records", f"{fraud_count:,}")
    c3.metric("Labelled fraud rate", f"{fraud_rate:.2f}%")
    c4.metric("Held-out F1-score", f"{metrics['f1_score']:.3f}")
    
    st.caption(
        "Demonstration project using synthetic, rule-labelled transactions. "
        "Results are not validated for real-world fraud detection."
    )

    st.divider()

    render_overview(df, FEATURE_COLUMNS)

elif selected_page == "🧪 Model Evaluation":
    render_model_evaluation(metrics, ARTIFACTS)

elif selected_page == "🔎 Predict Transaction":
    render_predictions(model)

elif selected_page == "📁 Batch Fraud Detection":
    render_batch_prediction(model, FEATURE_COLUMNS)

elif selected_page == "🗂️ Explore Data":
    render_data_explorer(df)

st.markdown(
    """
    <div class="dashboard-footer">
        Financial Fraud Intelligence · Educational ML demonstration · Synthetic data only
    </div>
    """,
    unsafe_allow_html=True,
)
