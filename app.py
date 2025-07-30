
import streamlit as st
import pandas as pd
from logic.meridien_model import run_meridien_model
from logic.future_planning import generate_future_plan
from logic.explain import explain_plan
from utils.chart_utils import plot_time_series, plot_forecast

st.set_page_config(page_title="📊 AIMMM – AI Marketing Mix Model", layout="wide")
st.title("📊 AIMMM – AI-Powered Marketing Mix Model")

uploaded_file = st.file_uploader("Upload your marketing CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Rename relevant columns to match internal model logic
        df.rename(columns={
            'Channel': 'media',
            'Actuals': 'spend',
            'NetRevenue': 'revenue',
        }, inplace=True)

        required_columns = {'media', 'spend', 'revenue'}
        if not required_columns.issubset(df.columns):
            st.error(f"Missing required columns. Found: {df.columns.tolist()}")
        else:
            st.success("File successfully processed!")

            st.subheader("📈 Time Series Trend")
            st.plotly_chart(plot_time_series(df), use_container_width=True)

            st.subheader("📊 MMM Output")
            roi_df, marginal_roi_df, normalized_roi_df = run_meridien_model(df)
            st.dataframe(roi_df)

            st.subheader("📑 Future Scenario Planner")
            plan_df = generate_future_plan(normalized_roi_df)
            st.dataframe(plan_df)

            st.subheader("📉 Forecasted Revenue Based on Plan")
            st.plotly_chart(plot_forecast(plan_df), use_container_width=True)

            st.download_button("📥 Download Plan CSV", data=plan_df.to_csv(index=False), file_name="media_plan.csv")

            st.subheader("🧠 Plan Explanation")
            st.markdown(explain_plan(plan_df))

    except Exception as e:
        st.error(f"Error processing the file: {e}")
