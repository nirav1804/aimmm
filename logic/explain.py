def explain_plan(plan_df):
    top_channel = plan_df.sort_values("expected_revenue", ascending=False).iloc[0]
    return f"The top performing channel in the forecasted plan is **{top_channel['media']}** with an expected revenue of ₹{top_channel['expected_revenue']:,.0f}."
