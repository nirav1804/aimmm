def generate_explanation(df):
    top_channels = df.sort_values("planned_spend", ascending=False).head(3)["media"].tolist()
    return f"The top 3 suggested media channels for investment are: {', '.join(top_channels)} based on their normalized ROI."
