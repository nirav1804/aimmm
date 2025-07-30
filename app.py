import streamlit as st
import pandas as pd
from logic.preprocess import preprocess_uploaded_file
from logic.meridien_model import run_meridien_model
from utils.chart_utils import plot_time_series, plot_forecast

st.set_page_config(page_title="📈 AI Media Mix Modeling", layout="wide")
st.title("📊 AI-Powered MMM: Media Optimization Tool")

uploaded_file = st.file_uploader("Upload your CSV file with Channel, Cost, Revenue", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        df = preprocess_uploaded_file(df)

        st.subheader("Cleaned Data Preview")
        st.dataframe(df.head())

        roi_df, marginal_roi_df, normalized_roi_df, forecast_df = run_meridien_model(df)

        st.subheader("📈 ROI Summary")
        st.dataframe(roi_df)

        st.subheader("📉 Marginal ROI")
        st.dataframe(marginal_roi_df)

        st.subheader("📊 Normalized ROI")
        st.dataframe(normalized_roi_df)

        st.subheader("📈 Forecasted Revenue")
        st.line_chart(forecast_df.set_index('media')['forecasted_revenue'])

        st.subheader("📤 Download Plan")
        st.download_button(
            label="Download ROI Plan as CSV",
            data=roi_df.to_csv(index=False),
            file_name="media_plan.csv",
            mime="text/csv"
        )

        st.subheader("📊 Trend Chart (Spends vs Revenue)")
        plot_time_series(df)

    except Exception as e:
        st.error(f"Error processing the file: {e}")
