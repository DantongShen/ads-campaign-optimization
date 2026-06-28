import streamlit as st
from pathlib import Path

IMG = Path(__file__).parent.parent.parent / "images"

st.set_page_config(page_title="Budget Optimization", layout="wide")
st.title("Channel and Budget Optimization")

st.markdown("""
This analysis models how shifting session volume across channels would affect projected revenue.
Because the dataset does not include ad spend, the model uses session count as a proxy for budget.
The goal is to identify directional reallocation candidates, not to compute exact ROI.
""")

st.markdown("---")

st.subheader("Diminishing Returns Model")
_, col, _ = st.columns([1, 3, 1])
with col:
    st.image(str(IMG / "diminishing_returns.png"), use_container_width=True)
st.markdown("""
Each channel's revenue response to session volume follows a power-law (diminishing returns) curve fitted from the historical data.
Referral has a steep curve, meaning each additional Referral session produces meaningful incremental revenue. Social flattens almost immediately: adding more Social sessions yields very little additional revenue past a low threshold.
This curve shapes the optimization: the model allocates sessions toward channels with higher marginal return.
""")

st.markdown("---")

st.subheader("Scenario Analysis")
st.markdown("""
Three interpretable reallocation scenarios were defined alongside a baseline. Each cuts Social and Affiliates (the most robust finding across all analysis), and differs in where the freed sessions are redirected.

| Scenario | Social | Affiliates | Referral | Paid Search | Display |
|---|---|---|---|---|---|
| Baseline | current | current | current | current | current |
| S1: Referral Priority | ×0.3 | ×0.3 | ×3.0 | unchanged | ×1.5 |
| S2: Paid Search Priority | ×0.3 | ×0.3 | unchanged | ×3.0 | ×1.5 |
| S3: Moderate Rebalance | ×0.5 | ×0.5 | ×2.0 | ×1.5 | ×1.5 |
""")
_, col, _ = st.columns([1, 3, 1])
with col:
    st.image(str(IMG / "scenario_analysis.png"), use_container_width=True)
_, col, _ = st.columns([1, 3, 1])
with col:
    st.image(str(IMG / "budget_reallocation.png"), use_container_width=True)

st.markdown("""
- All three scenarios beat baseline on projected revenue, but they involve different trade-offs
- S1 (Referral Priority) projects the highest total revenue (+\$74K vs baseline), but it uses more total sessions (373K vs 363K); part of the gain comes from more acquisition volume, not pure reallocation efficiency
- S2 (Paid Search Priority) has the highest revenue per session (\$3.71 vs \$2.49 baseline), but Social sessions are organic while Paid Search sessions carry a CPC; S2 only makes sense if the cost per Paid Search session is below the revenue it generates, which cannot be confirmed without spend data
- S3 (Moderate Rebalance) is the recommended starting point: +\$51K vs baseline with a less aggressive channel shift, making it the lowest-risk option before cost data is available
""")

st.markdown("---")

st.subheader("Channel Revenue Efficiency")
st.markdown("*For full channel performance breakdown, see the Traffic and Channel page.*")
_, col, _ = st.columns([1, 3, 1])
with col:
    st.image(str(IMG / "channel_revenue_per_session.png"), use_container_width=True)

st.markdown("""
- Referral log revenue coefficient is ~13x Paid Search; this is the clearest reallocation signal in the data
- The critical unknown is cost-per-session by channel, particularly whether Paid Search CPC is lower than revenue per Paid Search session
""")

st.markdown("---")

st.subheader("Recommendations")
st.markdown("""
- **Start with the Moderate Rebalance scenario:** halve Social and Affiliates, double Referral, grow Paid Search and Display 50%; this projects +\$51K revenue vs baseline and avoids over-rotating before cost data is available
- **Get cost-per-session data before committing to dollar-level reallocation:** the model optimizes session counts as a proxy; actual ROI depends on CPC for Paid Search and acquisition cost for Referral, neither of which is in this dataset
- **Treat Social as a reach channel, not a conversion channel:** do not evaluate Social on last-click revenue; if brand awareness is the goal, use reach and engagement metrics instead
- **Grow Referral through acquisition touchpoints, not ad spend:** Referral's high conversion rate comes from returning visitors; the right lever is more partnership and content placements that bring users back, not a paid Referral line item
""")
