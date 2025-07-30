def explain_results(roi_df):
    top_media = roi_df.sort_values("roi", ascending=False).iloc[0]
    low_media = roi_df.sort_values("roi", ascending=True).iloc[0]
    
    return f"""
Based on the ROI analysis:

- ✅ **Top-performing channel**: **{top_media['media']}** with an ROI of **{top_media['roi']:.2f}**
- ⚠️ **Least-performing channel**: **{low_media['media']}** with an ROI of **{low_media['roi']:.2f}**

It is advisable to increase spend on high-ROI channels and re-evaluate the performance strategy for lower ROI ones.
"""
