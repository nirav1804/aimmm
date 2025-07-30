import pandas as pd

def preprocess_uploaded_file(df):
    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Rename columns to expected names
    rename_dict = {
        'channel': 'media',
        'cost': 'spend',
        'revenue': 'revenue'
    }
    df = df.rename(columns=rename_dict)

    # Validation
    required_columns = {'media', 'spend', 'revenue'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Missing columns. Required columns are: {required_columns}")

    # Optional: clean data
    df = df.dropna(subset=['media', 'spend', 'revenue'])

    return df
