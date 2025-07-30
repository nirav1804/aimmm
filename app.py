import streamlit as st
import pandas as pd
from logic.preprocess import preprocess_data
from logic.mmm_model import run_mmm
from logic.forecasting import scenario_forecast
from logic.optimizer import optimize_budget
from logic.recommender import generate_insights
from utils.charts import plot_channel_rois, plot_channel_curves

st.set_page_config(layout="wide")
st.title("📊 AI-Powered Marketing Mix Modeling Platform")

uploaded_file = st.file_uploader("Upload media + revenue data", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    data, media_channels = preprocess_data(df)

    st.subheader("Step 1: ROI Analysis")
    roi_df, marginal_roi_df, normalized_roi_df = run_mmm(data, media_channels)
    st.dataframe(roi_df)

    plot_channel_rois(roi_df)

    st.subheader("Step 2: Objective Setting")
    obj = st.radio("Select your target", ["Revenue Target", "Spend Target", "ROI Target"])
    val = st.number_input("Enter Target Value (in INR)", min_value=0.0)

    strategy = st.selectbox("Select Strategy", ["Balanced", "Conservative", "Aggressive"])
    scenario_df = scenario_forecast(data, roi_df, obj, val, strategy)

    st.subheader("Recommended Media Plan")
    st.dataframe(scenario_df)

    st.subheader("Optimization Result (±20% variation)")
    optimized_df = optimize_budget(data, media_channels, roi_df, obj, val, strategy)
    st.dataframe(optimized_df)

    st.subheader("AI Insights")
    insights = generate_insights(roi_df, marginal_roi_df, normalized_roi_df)
    st.markdown(insights)

    st.subheader("Channel Performance Curves")
    plot_channel_curves(data, roi_df, media_channels)
