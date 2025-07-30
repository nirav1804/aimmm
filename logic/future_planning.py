import pandas as pd

def recommend_strategy(summary_df, mode, target):
    df = summary_df.copy()
    total_roi = (df['Contribution'].sum() / df['Spend'].sum()) if df['Spend'].sum() > 0 else 0

    if mode == 'Ad Spend Budget':
        df['Planned Spend'] = df['ROI'] / df['ROI'].sum() * target
    elif mode == 'Revenue Target':
        df['Planned Spend'] = (target / df['ROI'].sum()) * (df['ROI'] / df['ROI'].sum())
    elif mode == 'ROI Target':
        total_spend = df['Contribution'].sum() / target if target > 0 else 0
        df['Planned Spend'] = df['ROI'] / df['ROI'].sum() * total_spend

    df['Planned Spend'] = df['Planned Spend'].clip(lower=0.8 * df['Spend'], upper=1.2 * df['Spend'])
    return df[['Channel', 'Spend', 'Planned Spend']]
