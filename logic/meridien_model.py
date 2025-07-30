import pandas as pd
from sklearn.linear_model import LinearRegression

def run_meridien_model(df):
    spend_cols = [col for col in df.columns if '_spend' in col]
    X = df[spend_cols]
    y = df['revenue']

    model = LinearRegression().fit(X, y)
    coefficients = model.coef_
    intercept = model.intercept_ # The intercept is the baseline revenue not attributed to channels

    # Calculate predictions
    predictions = model.predict(X)

    # Calculate channel contributions over time
    channel_contributions = pd.DataFrame(index=df.index)
    for i, channel in enumerate(spend_cols):
        # Contribution for a channel at a given time point is its spend multiplied by its coefficient
        channel_contributions[channel.replace('_spend', '')] = X[channel] * coefficients[i]

    # Add back the intercept to each channel's contribution for total modeled revenue if desired,
    # or keep it separate as baseline. For individual channel contribution, we usually don't
    # distribute the intercept. The sum of channel_contributions + intercept should approximate predictions.
    # For reporting channel-wise ROI, we focus on the incremental revenue from that channel.

    summary = []
    for i, channel in enumerate(spend_cols):
        spend = X[channel].sum()
        # Sum of contributions for that channel across all time points
        contribution = channel_contributions[channel.replace('_spend', '')].sum()

        # ROI is total contribution from the channel divided by total spend on that channel
        roi = contribution / spend if spend > 0 else 0

        summary.append({
            'Channel': channel.replace('_spend', ''),
            'Spend': spend,
            'Contribution': contribution,
            'ROI': roi,
            'Marginal ROI': coefficients[i], # Marginal ROI is simply the coefficient
            'Normalized ROI': 0 # Placeholder, calculated after all ROIs are known
        })

    summary_df = pd.DataFrame(summary)

    # Calculate Normalized ROI: Scale ROI values between 0 and 1, relative to the max ROI.
    # This helps understand a channel's efficiency relative to the best performing one.
    max_roi = summary_df['ROI'].max()
    if max_roi > 0:
        summary_df['Normalized ROI'] = summary_df['ROI'] / max_roi
    else:
        summary_df['Normalized ROI'] = 0 # If all ROIs are zero or negative

    summary_df = summary_df.sort_values(by='ROI', ascending=False).reset_index(drop=True)

    # Include original 'date' column in channel_contributions for plotting if it exists
    if 'date' in df.columns:
        channel_contributions['date'] = df['date']
    else:
        # If no 'date' column, use the DataFrame index as a pseudo-date for plotting
        channel_contributions['date'] = df.index


    return model, summary_df, predictions, channel_contributions
