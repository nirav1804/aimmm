import pandas as pd

def run_meridien_model(df):
    required_columns = {"media", "spend", "revenue"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Missing columns. Required columns are: {required_columns}")

    roi_df = df.groupby("media").agg({"spend": "sum", "revenue": "sum"}).reset_index()
    roi_df["roi"] = roi_df["revenue"] / roi_df["spend"]

    marginal_roi_df = roi_df[["media", "roi"]].copy()
    marginal_roi_df["marginal_roi"] = marginal_roi_df["roi"] * 0.9

    normalized_roi_df = roi_df.copy()
    total_roi = normalized_roi_df["roi"].sum()
    normalized_roi_df["normalized_roi"] = normalized_roi_df["roi"] / total_roi

    return roi_df, marginal_roi_df, normalized_roi_df
