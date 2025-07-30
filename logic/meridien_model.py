import pandas as pd
from sklearn.linear_model import LinearRegression

def run_meridien_model(df):
    spend_cols = [col for col in df.columns if '_spend' in col]
    X = df[spend_cols]
    y = df['revenue']

    model = LinearRegression().fit(X, y)
    coefficients = model.coef_

    summary = []
    for i, channel in enumerate(spend_cols):
        spend = X[channel].sum()
        contribution = coefficients[i] * X[channel].sum()
        roi = contribution / spend if spend > 0 else 0
        summary.append({
            'Channel': channel.replace('_spend', ''),
            'Spend': spend,
            'Contribution': contribution,
            'ROI': roi,
            'Marginal ROI': coefficients[i],
            'Normalized ROI': roi / max(roi, 1)
        })

    summary_df = pd.DataFrame(summary).sort_values(by='ROI', ascending=False)
    return model, summary_df
