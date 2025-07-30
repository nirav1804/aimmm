import pandas as pd
import numpy as np

def generate_plan(roi_df, new_budget):
    total_roi = roi_df["ROI"].sum()
    roi_df["Budget Share"] = roi_df["ROI"] / total_roi
    roi_df["Planned Budget"] = roi_df["Budget Share"] * new_budget
    roi_df["Expected Contribution"] = roi_df["Planned Budget"] * roi_df["Marginal ROI"]
    return roi_df[["Channel", "Planned Budget", "Expected Contribution"]]
