import plotly.express as px

def plot_roi_barchart(df):
    fig = px.bar(df, x='media', y='roi', title="ROI by Media Channel")
    return fig

def plot_trend_chart(df):
    if 'date' not in df.columns:
        return None
    df['date'] = pd.to_datetime(df['date'])
    trend = df.groupby(['date', 'media'])[['spend']].sum().reset_index()
    fig = px.line(trend, x='date', y='spend', color='media', title="Spend Over Time by Media")
    return fig

def plot_forecast(forecast_df):
    fig = px.bar(forecast_df, x='media', y='expected_revenue', title="Forecasted Revenue by Media")
    return fig
