import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

def run_meridien_model(df, media_cols, target):
    X = df[media_cols].copy()
    y = df[target].values

    # Normalize the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = Ridge(alpha=0.5)
    model.fit(X_scaled, y)

    coef = model.coef_
    intercept = model.intercept_
    predictions = model.predict(X_scaled)

    result_df = df[media_cols].copy()
    result_df["Actual"] = y
    result_df["Predicted"] = predictions

    total_budget = X.sum(axis=0)
    contribution = coef * X.sum(axis=0)
    roi = contribution / total_budget
    marginal_roi = coef

    roi_df = pd.DataFrame({
        "Channel": media_cols,
        "Coefficient": coef,
        "Total Spend": total_budget,
        "Contribution": contribution,
        "ROI": roi,
        "Marginal ROI": marginal_roi
    })

    return result_df, roi_df
