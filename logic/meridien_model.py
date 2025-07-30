import pandas as pd

def run_meridien_model(df):
    grouped = df.groupby('media').agg(
        spend=('spend', 'sum'),
        revenue=('revenue', 'sum')
    ).reset_index()

    grouped['roi'] = grouped['revenue'] / grouped['spend']
    grouped['marginal_roi'] = grouped['roi'] - grouped['roi'].mean()
    grouped['normalized_roi'] = grouped['roi'] / grouped['roi'].sum()
    grouped['forecasted_revenue'] = grouped['spend'] * grouped['roi'] * 1.1  # Example 10% uplift

    return (
        grouped[['media', 'spend', 'revenue', 'roi']],
        grouped[['media', 'marginal_roi']],
        grouped[['media', 'normalized_roi']],
        grouped[['media', 'forecasted_revenue']]
    )
