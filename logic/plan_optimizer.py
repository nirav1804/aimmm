import pandas as pd

def optimize_plan(normalized_roi_df, total_budget):
    normalized_roi_df['allocated_spend'] = normalized_roi_df['normalized_roi'] * total_budget
    normalized_roi_df['expected_revenue'] = normalized_roi_df['allocated_spend'] * normalized_roi_df['roi']

    forecast = normalized_roi_df[['media', 'allocated_spend', 'expected_revenue']]
    forecast = forecast.rename(columns={'allocated_spend': 'budget'})

    return forecast, forecast
