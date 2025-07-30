import pandas as pd

def run_meridien_model(df):
    grouped = df.groupby('media').agg({'spend': 'sum', 'revenue': 'sum'}).reset_index()
    grouped['roi'] = grouped['revenue'] / grouped['spend']
    grouped['marginal_roi'] = grouped['roi'] * 0.8
    grouped['normalized_roi'] = grouped['roi'] / grouped['roi'].sum()

    roi_df = grouped[['media', 'spend', 'revenue', 'roi']]
    marginal_roi_df = grouped[['media', 'marginal_roi']]
    normalized_roi_df = grouped[['media', 'normalized_roi']]

    return roi_df, marginal_roi_df, normalized_roi_df
