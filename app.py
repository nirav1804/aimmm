import streamlit as st
import pandas as pd
from logic.meridien_model import run_meridien_model
from logic.future_planning import recommend_strategy
from logic.explain import generate_explanations
import altair as alt

st.set_page_config(page_title="MMM ROI Optimizer", layout="wide")
st.title("📊 Marketing Mix Modeling using Meridien")

uploaded_file = st.file_uploader("Upload 2-Year Marketing & Revenue Data (CSV)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")

    # Run MMM model
    results, summary_df = run_meridien_model(df)
    st.subheader("📈 Channel Performance Summary")
    st.dataframe(summary_df)

    # Graphs per channel
    st.subheader("📊 ROI vs Spend by Channel")
    chart = alt.Chart(summary_df).mark_bar().encode(
        x=alt.X('ROI:Q', title='ROI'),
        y=alt.Y('Channel:N', title='Channel'),
        color=alt.value('steelblue')
    )
    st.altair_chart(chart, use_container_width=True)

    # Explanation
    st.subheader("🧠 AI Explanation")
    for i, row in summary_df.iterrows():
        st.markdown(f"**{row['Channel']}**: {generate_explanations(row)}")

    # Future planning section
    st.subheader("📅 Future Planning")
    plan_type = st.selectbox("Choose Planning Goal", ["Revenue Target", "Ad Spend Budget", "ROI Target"])

    if plan_type == "Revenue Target":
        target = st.number_input("Enter Revenue Target (INR)", min_value=0)
    elif plan_type == "Ad Spend Budget":
        target = st.number_input("Enter Budget (INR)", min_value=0)
    else:
        target = st.number_input("Enter Target ROI", min_value=0.0, format="%.2f")

    if st.button("Generate Plan"):
        plan_df = recommend_strategy(summary_df, plan_type, target)
        st.write("🔁 Recommended Future Plan (±20% Max Change per Channel):")
        st.dataframe(plan_df)
