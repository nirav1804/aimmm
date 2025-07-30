import streamlit as st
import pandas as pd
import plotly.express as px
from logic.meridien_model import run_meridien_model
from logic.visualizations import plot_roi_barchart, plot_trend_chart, plot_forecast
from logic.plan_optimizer import optimize_plan

st.set_page_config(page_title="AI Marketing Mix Model", layout="wide")
st.title("📈 AI Marketing Mix Modeling & Budget Planner")

uploaded_file = st.file_uploader("Upload your campaign data CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # ✅ Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    st.subheader("Raw Data Preview")
    st.dataframe(df.head())

    try:
        roi_df, marginal_roi_df, normalized_roi_df = run_meridien_model(df)
    except ValueError as e:
        st.error(f"Error: {e}")
        st.stop()

    st.subheader("📊 ROI Summary")
    st.dataframe(roi_df)

    st.subheader("📉 Marginal ROI")
    st.dataframe(marginal_roi_df)

    st.subheader("⚖️ Normalized ROI")
    st.dataframe(normalized_roi_df)

    st.subheader("📈 Trend Charts")
    st.plotly_chart(plot_trend_chart(df), use_container_width=True)

    st.subheader("🧠 Budget Planner")
    total_budget = st.number_input("Enter Total Budget for Next Campaign", value=100000)
    optimized_plan, forecast = optimize_plan(normalized_roi_df, total_budget)

    st.subheader("Recommended Spend Plan")
    st.dataframe(optimized_plan)

    csv = optimized_plan.to_csv(index=False).encode('utf-8')
    st.download_button("Download Spend Plan CSV", csv, "optimized_plan.csv", "text/csv")

    st.subheader("📊 Forecasted Revenue from Plan")
    st.plotly_chart(plot_forecast(forecast), use_container_width=True)
