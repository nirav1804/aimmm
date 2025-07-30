**`logic/meridien_model.py`**
```python
import pandas as pd
from sklearn.linear_model import LinearRegression


def run_meridien_model(df):
    df = df.copy()
    df = df.dropna()

    y = df['Revenue']
    X = df.drop(columns=['Date', 'Revenue'])
    model = LinearRegression().fit(X, y)

    coefs = pd.Series(model.coef_, index=X.columns)
    roi = coefs / X.mean() * 100

    marginal_roi = coefs
    norm_roi = (roi - roi.min()) / (roi.max() - roi.min()) * 100

    roi_df = pd.DataFrame({
        'Channel': X.columns,
        'ROI': roi.values,
        'Marginal ROI': marginal_roi.values,
        'Normalized ROI': norm_roi.values
    })

    summary = pd.DataFrame({
        'Channel': X.columns,
        'Average Spend': X.mean().values,
        'Coefficient': coefs.values
    })

    return {'summary': summary, 'roi': roi_df, 'model': model, 'X': X, 'y': y}
```

---
