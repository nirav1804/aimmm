import pandas as pd

def generate_future_plan(normalized_roi_df, total_budget=1000000):
    normalized_roi_df['planned_spend'] = normalized_roi_df['normalized_roi'] * total_budget
    normalized_roi_df['expected_revenue'] = normalized_roi_df['planned_spend'] * 1.5
    return normalized_roi_df[['media', 'planned_spend', 'expected_revenue']]
