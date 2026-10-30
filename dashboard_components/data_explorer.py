import streamlit as st


def render_data_explorer(df):
    st.subheader("Explore transactions")

    filter_label = st.selectbox(
        "Choose transaction label",
        ["All", "Normal-labelled", "Fraud-labelled"],
    )

    if filter_label == "Fraud-labelled":
        filtered = df[df["is_fraud"] == 1]
    elif filter_label == "Normal-labelled":
        filtered = df[df["is_fraud"] == 0]
    else:
        filtered = df

    st.dataframe(filtered.head(500), use_container_width=True, height=400)

    st.download_button(
        "Download displayed data as CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="transaction_data.csv",
        mime="text/csv",
    )

    st.caption(
        f"{len(filtered):,} rows match the filter; "
        "the table displays at most 500 rows."
    )
