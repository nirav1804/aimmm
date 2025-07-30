def generate_explanations(row):
    if row['ROI'] > 1.5:
        return "This channel is delivering high returns on investment. Consider scaling this up."
    elif 1.0 < row['ROI'] <= 1.5:
        return "This channel is performing well. Maintain or test higher budgets."
    elif 0.5 < row['ROI'] <= 1.0:
        return "This channel has moderate ROI. Consider optimizing campaigns."
    else:
        return "Low performance channel. Reduce budget or reevaluate strategy."
