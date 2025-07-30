def generate_explanations(row):
    # Ensure numeric values are handled
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
    else: # roi < 0.5
        explanation += "This channel has low returns, potentially costing more than it earns. It requires a strategic review."

    # Marginal ROI commentary (indicating future potential)
    if marginal_roi > 0.5: # Arbitrary high value for very high marginal return
        explanation += " Its incremental impact on revenue is very high, suggesting that additional investment could yield significant returns."
    elif marginal_roi > 0.1: # Arbitrary moderate value
        explanation += " For every additional rupee spent, it brings in a good amount of extra revenue."
    elif marginal_roi > 0:
        explanation += " While its overall ROI might vary, each additional rupee spent still contributes positively to revenue."
    else: # marginal_roi <= 0
        explanation += " However, adding more budget to this channel currently shows diminishing or negative returns, so caution is advised for increasing spend."

    # Spend level commentary
    if spend == 0:
        explanation += " Currently, there's no spend in this channel, so its potential is untapped."

    return explanation
