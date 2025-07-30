import streamlit as st
import pandas as pd
from logic.meridien_model import run_meridien_model
from logic.preprocess import preprocess_data
from utils.chart_utils import plot_time_series, plot_forecast

st.set_page_config(page_title="📈 AI Marketing Planner", layout="wide")
st.title("📈 AI Marketing Planner using Marketing Mix Modeling (Meridien)")

uploaded_file = st.file_uploader("Upload your campaign performance CSV", type=["csv"])

if uploaded_file is not None:
    try:
        raw_df = pd.read_csv(uploaded_file)
        df = preprocess_data(raw_df)  # Smart renaming happens here

        roi_df, marginal_roi_df, normalized_roi_df, forecast_df = run_meridien_model(df)

        st.subheader("📊 ROI by Channel")
        st.dataframe(roi_df)

        st.subheader("🔍 Marginal ROI")
        st.dataframe(marginal_roi_df)

        st.subheader("📏 Normalized ROI")
        st.dataframe(normalized_roi_df)

        st.subheader("📥 Download Plan")
        csv = roi_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download ROI CSV", csv, "roi_plan.csv", "text/csv")

        st.subheader("📈 Time-Series Trends")
        st.plotly_chart(plot_time_series(df), use_container_width=True)

        st.subheader("📉 Forecasted Revenue based on current plan")
        st.plotly_chart(plot_forecast(forecast_df), use_container_width=True)

    except Exception as e:
        st.error(f"Error processing the file: {str(e)}")
else:
    st.info("👆 Upload a CSV file to get started.")
