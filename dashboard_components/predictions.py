import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.data import FEATURE_COLUMNS
from .styles import style_plotly_figure


def render_predictions(model):
    st.subheader("Analyze a transaction")
    st.write("Enter transaction details to obtain a model score.")

    with st.form("transaction_form"):
        c1, c2, c3 = st.columns(3)
        amount = c1.number_input("Transaction amount", min_value=0.01, value=250.0)
        hour = c2.slider("Hour of day", min_value=0, max_value=23, value=2)
        distance_home = c3.number_input(
            "Distance from home (km)", min_value=0.0, value=80.0
        )

        c1, c2, c3 = st.columns(3)
        distance_last = c1.number_input(
            "Distance from previous transaction (km)", min_value=0.0, value=50.0
        )
        ratio = c2.number_input(
            "Ratio to median purchase price", min_value=0.01, value=4.0
        )
        chip = c3.selectbox(
            "Chip used?", [0, 1], format_func=lambda x: "Yes" if x else "No"
        )

        c1, c2 = st.columns(2)
        pin = c1.selectbox(
            "PIN used?", [0, 1], format_func=lambda x: "Yes" if x else "No"
        )
        online = c2.selectbox(
            "Online order?", [0, 1], index=1,
            format_func=lambda x: "Yes" if x else "No"
        )

        submitted = st.form_submit_button("Analyze transaction", type="primary")

    if not submitted:
        return

    row = pd.DataFrame(
        [{
            "amount": amount,
            "hour": hour,
            "distance_from_home_km": distance_home,
            "distance_from_last_transaction_km": distance_last,
            "ratio_to_median_purchase_price": ratio,
            "used_chip": chip,
            "used_pin": pin,
            "online_order": online,
        }],
        columns=FEATURE_COLUMNS,
    )

    probability = float(model.predict_proba(row)[0, 1])
    predicted_label = int(probability >= 0.5)
    risk = "High" if probability >= 0.70 else "Medium" if probability >= 0.35 else "Low"

    c1, c2 = st.columns([1, 2])
    with c1:
        st.metric("Estimated model score", f"{probability:.1%}")
        st.metric("Demo risk band", risk)
        st.metric(
            "Predicted label",
            "Fraud-labelled" if predicted_label else "Normal-labelled",
        )

    with c2:
        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=probability * 100,
                number={"suffix": "%"},
                title={"text": "Model score (not calibrated real-world risk)"},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#E9DFFF"},
                    "bar": {"color": "#A78BFA"},
                    "bgcolor": "#171023",
                    "bordercolor": "#493267",
                    "steps": [
                        {"range": [0, 35], "color": "#241638"},
                        {"range": [35, 70], "color": "#4C1D95"},
                        {"range": [70, 100], "color": "#8B5CF6"},
                    ],
                },
            )
        )
        style_plotly_figure(gauge, height=350)
        st.plotly_chart(gauge, use_container_width=True)

    st.warning(
        "This is a synthetic-data demonstration. "
        "Do not use this score for real financial decisions."
    )
