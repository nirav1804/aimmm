import pandas as pd

def generate_plan(roi_df, total_budget=100000):
    plan_df = roi_df[["media", "roi"]].copy()
    total_roi = plan_df["roi"].sum()
    plan_df["allocated_budget"] = (plan_df["roi"] / total_roi) * total_budget
    return plan_df
