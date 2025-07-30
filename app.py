# app.py
import streamlit as st
import pandas as pd
from logic.meridien_model import run_meridien_model
from logic.future_planning import generate_plan
from logic.explain import explain_results
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="📈 Meridien MMM Tool", layout="wide")
st.title("📊 Marketing Mix Modeling (MMM) – Meridien")

uploaded_file = st.file_uploader("Upload your data CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("Data uploaded successfully!")

    if st.button("Run MMM Model"):
        roi_df, marginal_roi_df, normalized_roi_df = run_meridien_model(df)

        st.subheader("Channel-wise ROI")
        st.dataframe(roi_df)

        st.subheader("Marginal ROI")
        st.dataframe(marginal_roi_df)

        st.subheader("Normalized ROI")
        st.dataframe(normalized_roi_df)

        st.subheader("🔍 Easy Explanation")
        st.markdown(explain_results(roi_df))

        # Trend Charts
        st.subheader("📉 Time Series Trends")
        for channel in df.columns:
            if channel.lower() not in ["date", "revenue"]:
                fig, ax = plt.subplots()
                ax.plot(df[channel], label=channel)
                ax.set_title(f"Spend Trend – {channel}")
                st.pyplot(fig)

    st.markdown("---")
    st.subheader("📈 Future Planning")
    target_type = st.selectbox("Choose a target type", ["Revenue", "Ad Spend", "ROI"])
    user_input = st.number_input(f"Enter your {target_type} target (in INR):", min_value=0)

    plan_type = st.selectbox("Choose planning mode", ["Balanced", "Aggressive", "Conservative"])

    if st.button("Generate Future Plan"):
        plan_df, forecast_df, total_forecast = generate_plan(df, user_input, target_type, plan_type)

        st.subheader("📋 Recommended Media Plan")
        st.dataframe(plan_df)

        # Download button
        csv = plan_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Plan CSV", csv, "media_plan.csv", "text/csv")

        # Forecasted Revenue Bar Chart
        st.subheader("📊 Forecasted Revenue by Channel")
        fig, ax = plt.subplots()
        forecast_df.plot(kind="bar", x="Channel", y="Forecasted Revenue", ax=ax, legend=False)
        st.pyplot(fig)

        st.markdown(f"### 💰 Total Forecasted Revenue: ₹ {total_forecast:,.0f}")
