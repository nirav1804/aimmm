import pandas as pd

def preprocess_data(df):
    # Create a mapping based on common variations
    column_mapping = {
        "channel": "media",
        "media channel": "media",
        "spend": "spend",
        "spends": "spend",
        "amount spent": "spend",
        "cost": "spend",
        "revenue": "revenue",
        "sales": "revenue",
        "returns": "revenue"
    }

    # Convert all column names to lowercase
    df.columns = [col.lower().strip() for col in df.columns]

    # Rename based on mapping
    df = df.rename(columns={col: column_mapping.get(col, col) for col in df.columns})

    required_columns = {"media", "spend", "revenue"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Missing columns. Required columns are: {required_columns}")

    # Optional: Drop NaNs
    df = df.dropna(subset=["media", "spend", "revenue"])
    return df
