import streamlit as st
import pandas as pd
from logic.meridien_model import run_meridien_model
from logic.future_planning import generate_plan
from logic.explain import explain_results
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="📈 AI MMM Optimizer", layout="wide")
st.title("📊 AI Marketing Mix Model – Meridian Powered")

uploaded_file = st.file_uploader("Upload your campaign data (.csv)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Preprocessing: rename user columns to standard
    rename_map = {
        "Channel": "media",
        "Cost": "spend",
        "Sales": "revenue"
    }
    df = df.rename(columns=rename_map)

    try:
        roi_df, marginal_roi_df, normalized_roi_df = run_meridien_model(df)
        plan_df = generate_plan(roi_df)
        explanation = explain_results(roi_df)

        st.subheader("🔍 ROI by Channel")
        st.dataframe(roi_df)

        st.subheader("📈 Marginal ROI")
        st.dataframe(marginal_roi_df)

        st.subheader("⚖️ Normalized ROI")
        st.dataframe(normalized_roi_df)

        st.subheader("🚀 Recommended Future Spend Plan")
        st.dataframe(plan_df)

        st.subheader("🧠 AI Explanation")
        st.markdown(explanation)

    except Exception as e:
        st.error(f"Error processing the file: {e}")
