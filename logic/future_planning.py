**`logic/future_planning.py`**
```python
import pandas as pd
import numpy as np

def generate_plan(input_val, mode, strategy, model):
    weights = model.coef_ / sum(model.coef_)

    # Strategy multipliers
    if strategy == 'Balanced':
        adj = 1.0
    elif strategy == 'Aggressive':
        adj = 1.2
    else:  # Conservative
        adj = 0.8

    base_spends = weights * input_val * adj
    base_spends = np.clip(base_spends, base_spends * 0.8, base_spends * 1.2)  # ±20% variance

    forecast_revenue = model.predict([base_spends])[0]

    df_plan = pd.DataFrame({
        'Channel': model.feature_names_in_,
        'Proposed Spend': base_spends,
        'Weight': weights
    })

    df_forecast = pd.DataFrame({
        'Channel': model.feature_names_in_,
        'Forecasted Revenue': base_spends * model.coef_
    })

    return df_plan, df_forecast
```

---
