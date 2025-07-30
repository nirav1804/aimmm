**`logic/explain.py`**
```python
def generate_explanations(roi_df):
    explanations = {}
    for _, row in roi_df.iterrows():
        if row['ROI'] > 100:
            msg = "This channel is delivering excellent returns. Consider increasing its spend."
        elif row['ROI'] > 50:
            msg = "Moderate returns. Maintain or slightly increase investment."
        else:
            msg = "Low ROI. Review efficiency or reduce allocation."
        explanations[row['Channel']] = msg
    return explanations
```

---
