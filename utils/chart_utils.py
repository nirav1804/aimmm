import plotly.express as px

def plot_time_series(df):
    df_grouped = df.groupby('media').agg({'spend': 'sum', 'revenue': 'sum'}).reset_index()
    fig = px.bar(df_grouped, x='media', y=['spend', 'revenue'], barmode='group', title='Spend vs Revenue by Channel')
    return fig

def plot_forecast(df):
    fig = px.bar(df, x='media', y=['revenue', 'forecast'], barmode='group', title='Forecasted Revenue')
    return fig
