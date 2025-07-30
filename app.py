import streamlit as st
import pandas as pd
from logic.meridien_model import run_meridien_model
from logic.future_planning import scenario_planner
from logic.explain import generate_explanation
import matplotlib.pyplot as plt

st.set_page_config(page_title="📈 Marketing Mix Model", layout="wide")

st.title("📈 AI Marketing Mix Model – Powered by Meridian")

uploaded_file = st.file_uploader("Upload your marketing data CSV", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Rename columns to standard format
        df = df.rename(columns={
            "Media Channel": "media",
            "Weekly Spend": "spend",
            "Weekly Revenue": "revenue"
        })

        required_columns = {"media", "spend", "revenue"}
        if not required_columns.issubset(df.columns):
            raise ValueError(f"Missing columns. Required columns are: {required_columns}")

        # Show time series charts
        st.subheader("📊 Trend: Spend & Revenue")
        st.line_chart(df[["spend", "revenue"]])

        # Run core MMM model
        roi_df, marginal_roi_df, normalized_roi_df = run_meridien_model(df)

        st.subheader("🧠 ROI Summary")
        st.dataframe(roi_df)

        # Download ROI table
        st.download_button("📥 Download ROI Table as CSV", roi_df.to_csv(index=False), file_name="roi_results.csv")

        # Future planning
        st.subheader("🔮 Future Scenario Planning")
        budget = st.number_input("Enter planned total spend", min_value=1000, step=1000)
        if budget:
            plan_df, forecast = scenario_planner(normalized_roi_df, budget)
            st.dataframe(plan_df)

            # Download plan
            st.download_button("📥 Download Plan CSV", plan_df.to_csv(index=False), file_name="spend_plan.csv")

            # Forecast graph
            st.subheader("📈 Forecasted Revenue")
            fig, ax = plt.subplots()
            ax.bar(["Forecasted Revenue"], [forecast], color="green")
            ax.set_ylabel("Revenue")
            st.pyplot(fig)

            # Explanation
            st.subheader("💡 Explanation")
            st.markdown(generate_explanation(plan_df))

    except Exception as e:
        st.error(f"Error processing the file: {str(e)}")
