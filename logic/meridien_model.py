import pandas as pd

def run_meridien_model(df):
    # Basic aggregation
    grouped = df.groupby('media').agg({
        'spend': 'sum',
        'revenue': 'sum'
    }).reset_index()

    grouped['roi'] = grouped['revenue'] / grouped['spend']
    grouped['marginal_roi'] = grouped['roi'] - grouped['roi'].mean()
    grouped['normalized_roi'] = (grouped['roi'] - grouped['roi'].min()) / (grouped['roi'].max() - grouped['roi'].min())

    forecast_df = grouped[['media', 'revenue']].copy()
    forecast_df['forecast'] = forecast_df['revenue'] * 1.1  # Dummy forecast: +10%

    return grouped[['media', 'roi']], grouped[['media', 'marginal_roi']], grouped[['media', 'normalized_roi']], forecast_df
