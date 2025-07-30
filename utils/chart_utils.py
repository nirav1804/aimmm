import plotly.express as px
import pandas as pd

def plot_time_series(df):
    time_df = df.copy()
    if 'date' not in time_df.columns:
        time_df['date'] = pd.date_range(start='2023-01-01', periods=len(time_df))
    return px.line(time_df, x='date', y='spend', color='media', title="Spend Over Time")

def plot_forecast(plan_df):
    return px.bar(plan_df, x='media', y='expected_revenue', title="Forecasted Revenue by Media Channel", color='media')
