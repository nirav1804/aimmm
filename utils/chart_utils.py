import streamlit as st
import matplotlib.pyplot as plt

def plot_time_series(df):
    grouped = df.groupby('media')[['spend', 'revenue']].sum()
    grouped.plot(kind='bar', figsize=(10,5))
    st.pyplot(plt.gcf())

def plot_forecast(df):
    df.plot(kind='line', x='media', y='forecasted_revenue', marker='o')
    st.pyplot(plt.gcf())
