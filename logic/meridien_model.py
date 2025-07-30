# logic/meridien_model.py

import pandas as pd

def run_meridien_model(df):
    # Ensure the necessary columns exist
    required_columns = {'channel', 'spend', 'revenue'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Missing columns. Required columns are: {required_columns}")

    # Group by channel and calculate total spend and revenue
    grouped = df.groupby('channel').agg({
        'spend': 'sum',
        'revenue': 'sum'
    }).reset_index()

    # Calculate ROI: revenue / spend
    grouped['roi'] = grouped['revenue'] / grouped['spend']
    roi_df = grouped[['channel', 'spend', 'revenue', 'roi']]

    # Calculate marginal ROI assuming equal budget increments (dummy logic)
    total_spend = grouped['spend'].sum()
    grouped['marginal_roi'] = grouped['revenue'] / total_spend
    marginal_roi_df = grouped[['channel', 'marginal_roi']]

    # Normalize ROI scores to 0-1
    grouped['normalized_roi'] = (grouped['roi'] - grouped['roi'].min()) / (grouped['roi'].max() - grouped['roi'].min())
    normalized_roi_df = grouped[['channel', 'normalized_roi']]

    return roi_df, marginal_roi_df, normalized_roi_df
