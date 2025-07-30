import pandas as pd

def run_meridien_model(df):
    required_columns = {"media", "spend", "revenue"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Missing columns. Required columns are: {required_columns}")

    roi_df = df.groupby("media").agg({
        "spend": "sum",
        "revenue": "sum"
    }).reset_index()

    roi_df["roi"] = roi_df["revenue"] / roi_df["spend"]
    roi_df["marginal_roi"] = roi_df["roi"] * 0.8  # Placeholder logic
    roi_df["normalized_roi"] = roi_df["roi"] / roi_df["roi"].max()

    return roi_df[["media", "spend", "revenue", "roi"]], \
           roi_df[["media", "marginal_roi"]], \
           roi_df[["media", "normalized_roi"]]
