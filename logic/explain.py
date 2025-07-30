import pandas as pd # Import pandas to use pd.notna

def generate_explanations(row):
    # Ensure numeric values are handled and default to 0 if NaN/None
    roi = row['ROI'] if pd.notna(row['ROI']) else 0
    marginal_roi = row['Marginal ROI'] if pd.notna(row['Marginal ROI']) else 0
    spend = row['Spend'] if pd.notna(row['Spend']) else 0

    explanation = ""

    # General ROI commentary
    if roi >= 2.0:
        explanation += "This channel is incredibly efficient, delivering strong returns. It's a key growth driver."
    elif 1.0 < roi < 2.0:
        explanation += "This channel is performing well, generating more revenue than its cost. It's a reliable investment."
    elif 0.5 <= roi <= 1.0:
        explanation += "This channel's returns are moderate, nearing or at its cost. There might be room for optimization."
    else: # roi < 0.5 (or negative)
        explanation += "This channel has low returns, potentially costing more than it earns. It requires a strategic review."

    # Marginal ROI commentary (indicating future potential)
    # Use a small epsilon to avoid issues with floating point comparisons near zero
    epsilon = 1e-9
    if marginal_roi > 0.5 + epsilon: # Arbitrary high value for very high marginal return
        explanation += " Its incremental impact on revenue is very high, suggesting that additional investment could yield significant returns."
    elif marginal_roi > 0.1 + epsilon: # Arbitrary moderate value
        explanation += " For every additional rupee spent, it brings in a good amount of extra revenue."
    elif marginal_roi > epsilon: # marginal_roi is positive but small
        explanation += " While its overall ROI might vary, each additional rupee spent still contributes positively to revenue."
    else: # marginal_roi <= 0 (or very close to zero)
        explanation += " However, adding more budget to this channel currently shows diminishing or negative returns, so caution is advised for increasing spend."

    # Spend level commentary
    if spend == 0:
        explanation += " Currently, there's no spend in this channel, so its potential is untapped."

    return explanation
