import pandas as pd

def preprocess_data(df):
    column_mapping = {
        'channel': 'media',
        'media channel': 'media',
        'media': 'media',

        'spend': 'spend',
        'spends': 'spend',
        'investment': 'spend',
        'budget': 'spend',

        'revenue': 'revenue',
        'sales': 'revenue',
        'revenue generated': 'revenue'
    }

    # Normalize column names
    df.columns = [col.strip().lower() for col in df.columns]

    # Rename using mapping
    df.rename(columns=lambda x: column_mapping.get(x.strip().lower(), x), inplace=True)

    required_cols = {'media', 'spend', 'revenue'}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Missing columns. Required columns are: {required_cols}")

    return df
