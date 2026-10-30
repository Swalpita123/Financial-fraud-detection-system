
import streamlit as st
import pandas as pd


def render_batch_prediction(model, feature_columns):

    st.subheader("Batch Fraud Detection")

    st.caption(
        "Upload a CSV or Excel file to predict potentially "
        "fraudulent transactions."
    )

    uploaded_file = st.file_uploader(
        "Upload Transaction File",
        type=["csv", "xlsx"],
    )

    if uploaded_file is None:
        st.info("Upload a transaction file to start batch prediction.")
        return

    try:
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)

        st.success("File uploaded successfully!")

        st.write("Uploaded Data Preview")

        st.dataframe(
            data.head(10),
            use_container_width=True,
        )

        # Validate required features
        missing_columns = [
            col for col in feature_columns
            if col not in data.columns
        ]

        if missing_columns:
            st.error(
                f"Missing required columns: {missing_columns}"
            )
            return

        if data.empty:
            st.warning("The uploaded file contains no transactions.")
            return

        # Select features in the exact training order
        X = data[feature_columns].copy()

        # Validate numeric feature values
        X = X.apply(pd.to_numeric, errors="coerce")

        if X.isnull().any().any():
            st.error(
                "Missing or invalid feature values found. "
                "Please clean the uploaded file."
            )
            return

        # Batch prediction
        predictions = model.predict(X)

        probabilities = model.predict_proba(X)[:, 1]

        # Add prediction results
        results = data.copy()

        results["fraud_prediction"] = predictions

        results["fraud_probability"] = (
            probabilities * 100
        ).round(2)

        results["prediction_label"] = results[
            "fraud_prediction"
        ].map({
            0: "Normal",
            1: "Potential Fraud",
        })

        # Summary
        fraud_count = int((predictions == 1).sum())

        normal_count = int((predictions == 0).sum())

        st.divider()

        st.subheader("Prediction Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Transactions",
            f"{len(results):,}",
        )

        col2.metric(
            "Normal",
            f"{normal_count:,}",
        )

        col3.metric(
            "Potential Fraud",
            f"{fraud_count:,}",
        )

        # Results table
        st.subheader("Prediction Results")

        st.dataframe(
            results,
            use_container_width=True,
            height=400,
        )

        # Fraud records
        fraud_records = results[
            results["fraud_prediction"] == 1
        ]

        st.subheader("Potential Fraud Transactions")

        st.dataframe(
            fraud_records,
            use_container_width=True,
        )

        # Download predictions
        csv_data = results.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "Download Prediction Results",
            data=csv_data,
            file_name="fraud_prediction_results.csv",
            mime="text/csv",
            use_container_width=True,
        )

    except Exception as e:
        st.error(f"Prediction failed: {e}")
