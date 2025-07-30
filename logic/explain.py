def explain_results(plan_df):
    explanations = []
    for _, row in plan_df.iterrows():
        channel = row["Channel"]
        budget = row["Planned Budget"]
        contribution = row["Expected Contribution"]

        if contribution > budget:
            comment = f"{channel} has a strong ROI. Recommended increased spend."
        else:
            comment = f"{channel} has lower returns. Consider optimizing or reallocating spend."

        explanations.append({
            "Channel": channel,
            "Budget": round(budget, 2),
            "Contribution": round(contribution, 2),
            "Comment": comment
        })

    return explanations
