import pandas as pd
import streamlit as st # Import streamlit to use st.warning

def recommend_strategy(summary_df, mode, target):
    df = summary_df.copy()

    # Calculate current total spend and current total contribution
    current_total_spend = df['Spend'].sum()
    current_total_contribution = df['Contribution'].sum()

    # Initialize 'Planned Spend' column
    df['Planned Spend'] = df['Spend'] # Start with current spend

    # A simple allocation logic: distribute budget based on Marginal ROI (coefficient)
    # Channels with higher marginal ROI get a larger share of the incremental budget/target.
    # To avoid division by zero if all marginal ROIs are zero or negative, handle this.
    positive_marginal_roi_sum = df[df['Marginal ROI'] > 0]['Marginal ROI'].sum()

    if mode == 'Ad Spend Budget':
        # If target budget is less than current spend, we need to scale down
        # If target budget is more than current spend, we need to scale up
        budget_difference = target - current_total_spend

        if positive_marginal_roi_sum > 0:
            # Allocate budget difference based on marginal ROI
            df['Planned Spend'] = df['Spend'] + (df['Marginal ROI'] / positive_marginal_roi_sum) * budget_difference
        else:
            # If no positive marginal ROI, distribute equally or based on current proportion
            df['Planned Spend'] = (df['Spend'] / current_total_spend) * target if current_total_spend > 0 else target / len(df)


    elif mode == 'Revenue Target':
        # Estimate the total spend required to hit the revenue target
        # Assuming average ROI (total contribution / total spend) can be used as a proxy
        # This is a simplification; a more complex model would iterate.
        current_overall_roi = current_total_contribution / current_total_spend if current_total_spend > 0 else 0
        
        # If current_overall_roi is 0 or very small, this calculation can be problematic.
        # Fallback to a simple proportional scaling if ROI is not meaningful.
        if current_overall_roi > 0:
            estimated_total_spend_needed = target / current_overall_roi
            # Allocate this estimated total spend based on marginal ROI if available, else current proportion
            spend_difference = estimated_total_spend_needed - current_total_spend
            if positive_marginal_roi_sum > 0:
                 df['Planned Spend'] = df['Spend'] + (df['Marginal ROI'] / positive_marginal_roi_sum) * spend_difference
            else:
                 df['Planned Spend'] = (df['Spend'] / current_total_spend) * estimated_total_spend_needed if current_total_spend > 0 else estimated_total_spend_needed / len(df)
        else:
            st.warning("Cannot calculate spend for revenue target due to zero or negative overall ROI. Proposing proportional spend increase based on current spend.")
            # If no meaningful ROI, simply scale up spend proportionally to revenue target vs current revenue
            # This assumes df['revenue'] refers to the total revenue from the original data, not just what's in summary_df
            # To get original total revenue, we'd need to pass the original df or its total revenue sum.
            # For simplicity here, if current_overall_roi is bad, we just make minimal changes or return current spend.
            df['Planned Spend'] = df['Spend'] # No change if cannot calculate reliably.
            # A better approach would be to pass original df or its total revenue to this function.


    elif mode == 'ROI Target':
        # This is more complex as it's an optimization problem.
        # Simplification: adjust spend to move towards the target ROI for each channel,
        # weighted by marginal ROI to prioritize efficient channels.
        # If we want a global ROI target, we need to find total spend that yields that ROI.

        # Let's target the *average* channel ROI to move towards the global target.
        # This is a heuristic, not a true optimization.
        if target > 0 and current_total_contribution > 0:
            estimated_total_spend = current_total_contribution / target # Total spend needed to achieve target ROI
            spend_difference = estimated_total_spend - current_total_spend

            if positive_marginal_roi_sum > 0:
                 df['Planned Spend'] = df['Spend'] + (df['Marginal ROI'] / positive_marginal_roi_sum) * spend_difference
            else:
                 df['Planned Spend'] = (df['Spend'] / current_total_spend) * estimated_total_spend if current_total_spend > 0 else estimated_total_spend / len(df)

        else:
            st.warning("Cannot calculate spend for ROI target (target ROI is zero or no contributions). Proposing no change.")
            df['Planned Spend'] = df['Spend'] # No change if cannot calculate reliably.


    # Apply the +/- 20% variance constraint
    df['Planned Spend'] = df.apply(
        lambda row: max(0.8 * row['Spend'], min(1.2 * row['Spend'], row['Planned Spend'])),
        axis=1
    )
    # Ensure no negative planned spend
    df['Planned Spend'] = df['Planned Spend'].clip(lower=0)

    return df[['Channel', 'Spend', 'Planned Spend']]
