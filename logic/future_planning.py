import pandas as pd

def scenario_planner(normalized_roi_df, budget):
    normalized_roi_df = normalized_roi_df.copy()
    total_weight = normalized_roi_df["normalized_roi"].sum()
    normalized_roi_df["planned_spend"] = (normalized_roi_df["normalized_roi"] / total_weight) * budget
    normalized_roi_df["forecasted_revenue"] = normalized_roi_df["planned_spend"] * normalized_roi_df["normalized_roi"] * 2  # Placeholder
    forecast = normalized_roi_df["forecasted_revenue"].sum()
    return normalized_roi_df, forecast
