import pandas as pd
import plotly.express as px
import streamlit as st

from .styles import style_plotly_figure

CHART_HEIGHT = 400

CHART_MARGIN = dict(
    l=25,
    r=25,
    t=60,
    b=65,
)


def render_overview(df, feature_columns):

    st.subheader("Transaction Analytics")

    # ==========================================
    # ROW 1: TRANSACTION AMOUNT + HOURLY FRAUD
    # ==========================================

    left, right = st.columns(2, gap="large")

    # LEFT: Transaction Amount Distribution
    with left:

        amount_fig = px.histogram(
            df,
            x="amount",
            color="is_fraud",
            nbins=45,
            barmode="overlay",
            opacity=0.7,
            color_discrete_map={
                0: "#A78BFA",
                1: "#E9D5FF",
            },
            title="Transaction Amount Distribution",
            labels={
                "amount": "Transaction amount",
                "is_fraud": "Synthetic label",
            },
        )

        style_plotly_figure(
            amount_fig,
            height=CHART_HEIGHT,
        )

        amount_fig.update_layout(
            margin=CHART_MARGIN,
            legend_title_text="Transaction label",
        )

        st.plotly_chart(
            amount_fig,
            use_container_width=True,
            config={"responsive": True},
        )

    # RIGHT: Fraud Label Rate by Hour
    with right:

        hourly = df.groupby(
            "hour",
            as_index=False,
        ).agg(
            fraud_rate=("is_fraud", "mean"),
            transaction_count=("is_fraud", "size"),
        )

        hourly_fig = px.bar(
            hourly,
            x="hour",
            y="fraud_rate",
            hover_data=["transaction_count"],
            title="Fraud-Label Rate by Hour",
            labels={
                "hour": "Hour of day",
                "fraud_rate": "Fraud-label rate",
                "transaction_count": "Transactions",
            },
            color="fraud_rate",
            color_continuous_scale=[
                [0.0, "#4C1D95"],
                [0.5, "#8B5CF6"],
                [1.0, "#E9D5FF"],
            ],
        )

        style_plotly_figure(
            hourly_fig,
            height=CHART_HEIGHT,
        )

        hourly_fig.update_layout(
            margin=CHART_MARGIN,
            coloraxis_showscale=False,
        )

        hourly_fig.update_xaxes(dtick=2)
        hourly_fig.update_yaxes(tickformat=".0%")

        st.plotly_chart(
            hourly_fig,
            use_container_width=True,
            config={"responsive": True},
        )

    # ==========================================
    # ROW 2: TRANSACTION FEATURES + CORRELATION
    # ==========================================

    left, right = st.columns(2, gap="large")

    # LEFT: Transaction Feature Distribution
    with left:

        signal_data = pd.DataFrame(
            {
                "Signal": [
                    "Chip used",
                    "PIN used",
                    "Online order",
                ],
                "Share": [
                    df["used_chip"].mean(),
                    df["used_pin"].mean(),
                    df["online_order"].mean(),
                ],
            }
        )

        signal_fig = px.bar(
            signal_data,
            x="Signal",
            y="Share",
            title="Transaction Feature Distribution",
            color="Signal",
            color_discrete_sequence=[
                "#6D28D9",
                "#A78BFA",
                "#DDD6FE",
            ],
        )

        style_plotly_figure(
            signal_fig,
            height=CHART_HEIGHT,
        )

        signal_fig.update_layout(
            margin=CHART_MARGIN,
            showlegend=False,
        )

        signal_fig.update_yaxes(
            tickformat=".0%",
        )

        st.plotly_chart(
            signal_fig,
            use_container_width=True,
            config={"responsive": True},
        )

    # RIGHT: Feature Correlation with Fraud
    with right:

        correlation = df[feature_columns + ["is_fraud"]].corr(numeric_only=True)

        # Get each feature's correlation with fraud
        correlation_data = correlation["is_fraud"].drop("is_fraud").reset_index()

        correlation_data.columns = [
            "Feature",
            "Correlation",
        ]

        correlation_data["Strength"] = correlation_data["Correlation"].abs()

        # Purple color palette
        purple_colors = [
            "#48109B",
            "#5D23BB",
            "#823DF9",
            "#8053EB",
            "#997BF4",
            "#AA98F3",
            "#C7BEF1",
            "#C9B7DD",
        ]

        correlation_fig = px.pie(
            correlation_data,
            names="Feature",
            values="Strength",
            hole=0.48,
            color="Feature",
            color_discrete_sequence=purple_colors,
            title="Feature Correlation with Fraud",
        )

        # Correlation details on hover
        correlation_fig.update_traces(
            customdata=correlation_data[["Correlation"]].values,
            textposition="inside",
            textinfo="percent",
            textfont=dict(
                size=12,
                color="#FFFFFF",
                family="Inter",
            ),
            marker=dict(
                line=dict(
                    color="#171023",
                    width=3,
                )
            ),
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Correlation: %{customdata[0]:.3f}<br>"
                "Relative strength: %{percent}"
                "<extra></extra>"
            ),
        )

        style_plotly_figure(
            correlation_fig,
            height=CHART_HEIGHT,
        )

        correlation_fig.update_layout(
            title=dict(
                text="Feature Correlation with Fraud",
                font=dict(
                    size=17,
                    color="#E9DFFF",
                ),
            ),
            showlegend=True,
            legend=dict(
                orientation="v",
                x=1.02,
                y=0.5,
                font=dict(
                    size=10,
                    color="#E9DFFF",
                ),
            ),
            margin=dict(
                l=20,
                r=130,
                t=65,
                b=20,
            ),
            # Match the other dashboard charts
            paper_bgcolor="#171023",
            plot_bgcolor="#171023",
            font=dict(
                family="Inter",
                color="#E9DFFF",
            ),
        )

        st.plotly_chart(
            correlation_fig,
            use_container_width=True,
            config={"responsive": True},
        )
