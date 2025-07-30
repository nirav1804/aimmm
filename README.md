# 📊 Marketing Mix Modeling using Meridien

This is a Streamlit-based tool for ROI-driven marketing mix modeling using linear regression. It reads 2 years of weekly spend and revenue data and outputs insights including:

- Channel-wise ROI, Marginal ROI, and Normalized ROI
- Simple explanations per channel
- Future planning tools with budget/revenue/ROI target
- Enhanced visualizations for deeper insights.

## 🧠 Features
- Linear Regression-based MMM using `scikit-learn`
- Smart planning suggestions with a +/- 20% variance constraint per channel
- Enhanced Visualizations with Altair, including:
    - Actual vs. Predicted Revenue over time
    - Normalized Channel Contribution over time
    - Overall Channel Contribution Breakdown (Pie Chart)
    - Current vs. Planned Spend comparison for future strategies
- Streamlit frontend for interactive use

## 🚀 Usage

To run this application locally:

```bash
# 1. Ensure you have Python installed.
# 2. Navigate to the directory where you saved these files.
# 3. Install the required Python libraries:
pip install -r requirements.txt

# 4. Run the Streamlit application:
streamlit run app.py
