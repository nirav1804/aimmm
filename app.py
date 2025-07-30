import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set page config
st.set_page_config(page_title="📈 Simple MMM App", layout="wide")

st.title("📊 Marketing Mix Modeling (MMM) – Long Format Auto Converter")

# Upload file
uploaded_file = st.file_uploader("📤 Upload your media spend CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip()  # Clean column names

        # Required columns
        spend_cols = [col for col in df.columns if col.endswith("_spend")]
        required_cols = ['date_start', 'revenue'] + spend_cols

        # Check for required columns
        if not set(required_cols).issubset(df.columns):
            missing = set(required_cols) - set(df.columns)
            st.error(f"❌ Missing columns in your file: {missing}")
            st.stop()

        # Melt to long format
        df_melted = df.melt(
            id_vars=['date_start', 'revenue'],
            value_vars=spend_cols,
            var_name='media',
            value_name='spend'
        )

        df_melted = df_melted.dropna(subset=['spend', 'revenue'])

        # Optional cleaning
        df_melted['media'] = df_melted['media'].str.replace('_spend', '', regex=False)

        st.subheader("🧹 Preview: Melted Data (Long Format)")
        st.dataframe(df_melted.head(10))

        # MMM modeling - very simple linear regression
        st.subheader("📉 Simple ROI Analysis")

        roi_df = df_melted.groupby('media').agg(
            total_spend=('spend', 'sum'),
            total_revenue=('revenue', 'sum')
        ).reset_index()

        roi_df['ROI'] = roi_df['total_revenue'] / roi_df['total_spend']
        roi_df = roi_df.sort_values(by='ROI', ascending=False)

        st.dataframe(roi_df)

        # 📊 ROI Chart
        st.subheader("📊 ROI by Channel")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=roi_df, x='ROI', y='media', ax=ax, palette='viridis')
        ax.set_title("Channel-wise ROI")
        st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error processing the file: {str(e)}")
else:
    st.info("👆 Please upload a `.csv` file with date_start, revenue, and *_spend columns.")

