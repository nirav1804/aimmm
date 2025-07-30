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
    # Ensure 'date' column is present or create an index-based 'date' for plotting
    if 'date' not in df.columns:
        df['date'] = df.index # Use DataFrame index as 'date' if not provided

    model, summary_df, predictions, channel_contributions_df = run_meridien_model(df)
    st.subheader("📈 Channel Performance Summary")

    if st.checkbox("Show all channels including zero spend?"):
        st.dataframe(summary_df)
    else:
        st.dataframe(summary_df[summary_df['Spend'] > 0])

    # New: Actual vs Predicted Revenue Chart
    st.subheader("📊 Actual vs. Predicted Revenue Over Time")
    plot_df = pd.DataFrame({'Date': pd.to_datetime(df['date']), 'Actual Revenue': df['revenue'], 'Predicted Revenue': predictions})

    actual_chart = alt.Chart(plot_df).mark_line(color='blue').encode(
        x=alt.X('Date:T', title='Date/Index'),
        y=alt.Y('Actual Revenue:Q', title='Revenue'),
        tooltip=[alt.Tooltip('Date:T', format='%Y-%m-%d'), 'Actual Revenue']
    )
    predicted_chart = alt.Chart(plot_df).mark_line(color='red').encode(
        x=alt.X('Date:T', title='Date/Index'),
        y=alt.Y('Predicted Revenue:Q', title='Revenue'),
        tooltip=[alt.Tooltip('Date:T', format='%Y-%m-%d'), 'Predicted Revenue']
    )
    st.altair_chart(actual_chart + predicted_chart, use_container_width=True)
    st.markdown("---")


    # New: Channel Contribution Over Time
    st.subheader("📊 Channel Contribution Over Time (Normalized)")
    contributions_melted = channel_contributions_df.reset_index().melt(id_vars=['date'], var_name='Channel', value_name='Contribution')
    contributions_melted['date'] = pd.to_datetime(contributions_melted['date']) # Ensure date is datetime

    # Calculate normalized contribution
    contributions_melted['Normalized Contribution'] = contributions_melted.groupby('date')['Contribution'].transform(lambda x: x / x.sum())

    contribution_chart = alt.Chart(contributions_melted).mark_area().encode(
        x=alt.X('date:T', title='Date/Index'),
        y=alt.Y('Normalized Contribution:Q', stack='normalize', title='Normalized Contribution'),
        color='Channel:N',
        tooltip=[alt.Tooltip('date:T', format='%Y-%m-%d'), 'Channel:N', alt.Tooltip('Contribution:Q', format='.2f')] # Show actual contribution in tooltip
    ).properties(
        title='Normalized Channel Contribution Over Time'
    )
    st.altair_chart(contribution_chart, use_container_width=True)
    st.markdown("---")

    # Graphs per channel (Original ROI vs Spend chart)
    st.subheader("📊 ROI vs Spend by Channel")
    chart = alt.Chart(summary_df).mark_bar().encode(
        x=alt.X('ROI:Q', title='ROI'),
        y=alt.Y('Channel:N', title='Channel', sort='-x'), # Sort by ROI
        color=alt.value('steelblue'),
        tooltip=['Channel', alt.Tooltip('Spend', format='.2f'), alt.Tooltip('ROI', format='.2f'), alt.Tooltip('Marginal ROI', format='.2f')]
    )
    text = chart.mark_text(
        align='left',
        baseline='middle',
        dx=3 # Nudge text to the right
    ).encode(
        text=alt.Text('ROI:Q', format='.2f'),
        color=alt.value('black')
    )
    st.altair_chart(chart + text, use_container_width=True)
    st.markdown("---")

    # New: Overall Channel Contribution Breakdown
    st.subheader("📊 Overall Channel Contribution Breakdown")
    # Ensure no negative contributions affect pie chart
    positive_contribution_df = summary_df[summary_df['Contribution'] > 0].copy()
    total_positive_contribution = positive_contribution_df['Contribution'].sum()

    if total_positive_contribution > 0:
        positive_contribution_df['Percentage'] = positive_contribution_df['Contribution'] / total_positive_contribution

        pie_chart = alt.Chart(positive_contribution_df).mark_arc(outerRadius=120).encode(
            theta=alt.Theta("Percentage", stack=True),
            color=alt.Color("Channel"),
            order=alt.Order("Percentage", sort="descending"),
            tooltip=["Channel", alt.Tooltip("Percentage", format=".1%"), alt.Tooltip("Contribution", format=".2f")]
        ).properties(
            title='Total Revenue Contribution by Channel (Positive Contributions Only)'
        )
        text_labels = pie_chart.mark_text(radius=140).encode(
            text=alt.Text("Percentage", format=".1%"),
            order=alt.Order("Percentage", sort="descending"),
            color=alt.value("black") # Set text color to black
        )
        st.altair_chart(pie_chart + text_labels, use_container_width=True)
    else:
        st.info("No positive channel contributions to display in the pie chart.")
    st.markdown("---")


    # Explanation
    st.subheader("🧠 AI Explanation")
    for i, row in summary_df.iterrows():
        st.markdown(f"**{row['Channel']}**: {generate_explanations(row)}")
    st.markdown("---")

    # Future planning section
    st.subheader("📅 Future Planning")
    plan_type = st.selectbox("Choose Planning Goal", ["Revenue Target", "Ad Spend Budget", "ROI Target"])

    # Extract spend_cols from the original dataframe for default values
    spend_cols = [col for col in df.columns if '_spend' in col]

    target = 0.0
    if plan_type == "Revenue Target":
        # Default to 10% increase from current total revenue
        current_total_revenue = df['revenue'].sum()
        target = st.number_input("Enter Revenue Target (INR)", min_value=0.0, value=current_total_revenue * 1.1, format="%.2f")
    elif plan_type == "Ad Spend Budget":
        # Default to 10% increase from current total ad spend
        current_total_spend = df[spend_cols].sum().sum()
        target = st.number_input("Enter Budget (INR)", min_value=0.0, value=current_total_spend * 1.1, format="%.2f")
    else: # ROI Target
        # Default to 10% increase from current average ROI (of channels with spend > 0)
        current_average_roi = summary_df[summary_df['Spend'] > 0]['ROI'].mean()
        target = st.number_input("Enter Target ROI", min_value=0.0, value=current_average_roi * 1.1 if not pd.isna(current_average_roi) else 0.0, format="%.2f")

    if st.button("Generate Plan"):
        plan_df = recommend_strategy(summary_df, plan_type, target)
        st.write("🔁 Recommended Future Plan (±20% Max Change per Channel):")
        st.dataframe(plan_df)

        # New: Current vs. Planned Spend Chart
        st.subheader("📊 Current vs. Planned Spend per Channel")
        plan_chart_df = plan_df.melt(id_vars=['Channel'], var_name='Spend Type', value_name='Amount')
        plan_chart = alt.Chart(plan_chart_df).mark_bar().encode(
            x=alt.X('Spend Type:N', title=''), # No title for x-axis as it's grouped
            y=alt.Y('Amount:Q', title='Spend (INR)'),
            color='Spend Type:N',
            column=alt.Column('Channel:N', header=alt.Header(titleOrient="bottom", labelOrient="bottom")),
            tooltip=['Channel', 'Spend Type', alt.Tooltip('Amount', format='.2f')]
        ).properties(
            title='Current vs. Planned Spend by Channel'
        ).resolve_scale(
            x="independent"
        )
        st.altair_chart(plan_chart, use_container_width=True)
