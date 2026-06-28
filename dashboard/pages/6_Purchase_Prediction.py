import streamlit as st
from pathlib import Path

IMG = Path(__file__).parent.parent.parent / "images"

st.set_page_config(page_title="Purchase Prediction", layout="wide")
st.title("Purchase Prediction")
st.markdown("The funnel and channel analyses describe what happened in aggregate. This page goes one level deeper: using session-level features to predict whether an individual session will result in a purchase, and to quantify which factors matter most. Three models were trained and compared (Logistic Regression, Random Forest, and Gradient Boosting), with results feeding directly back into the channel and audience targeting recommendations.")

st.markdown("---")

st.subheader("Model Comparison (ROC Curves)")
col1, col2 = st.columns([2, 1])
with col1:
    st.image(str(IMG / "roc_comparison.png"), use_container_width=True)
with col2:
    st.markdown("**AUC-ROC Results**")
    st.markdown("""
| Model | AUC-ROC |
|---|---|
| Logistic Regression | 0.9828 |
| Random Forest | 0.9860 |
| Gradient Boosting | 0.9863 |
""")

st.markdown("""
- The ~0.004 gap between LR and GB confirms the signal is largely linear; LR captures most of it already
- Low precision (0.18 to 0.21) is a base rate problem, not a model problem: at 1.30% conversion rate, even a well-calibrated model flags many non-buyers; use the raw probability score for ranking sessions rather than a binary prediction
""")

st.markdown("---")

st.subheader("Feature Importance")
st.image(str(IMG / "feature_importance.png"), use_container_width=True)

st.markdown("""
- Top three predictors across all models: `is_us`, `pageviews`, `is_returning`; geography and engagement depth dominate, channel and time features are secondary once visitor behavior is known
- `ch_Referral` coefficient is near zero after controlling for `is_returning`: Referral's 6.25% raw conversion rate is returning visitor behavior, not a channel effect
- `ch_Affiliates` is the strongest negative predictor: worst channel even after controlling for all session characteristics, consistent with the budget optimization recommendation to cut it
- Feature ranking shifts between model types: LR ranks `is_us` first; tree models rank `pageviews` first; RF spreads importance across `pageviews` and `time_on_site` (77% combined), while GB concentrates ~85% on `pageviews` alone
""")

st.markdown("---")

st.subheader("Recommendations")
st.markdown("""
- **Use probability scores, not binary predictions:** rank sessions by predicted purchase probability to prioritize high-intent users for retargeting or personalization; a binary threshold at 1.30% base rate will produce too many false positives to be actionable
- **Prioritize US returning visitors with high pageview counts:** these three features dominate all models; targeting sessions that are US-based, have 10+ pageviews, and are returning visitors will capture the highest-probability buyers
- **Do not attribute Referral's conversion rate to the channel:** after controlling for returning visitor status, the channel effect disappears; Referral works because it brings back returning visitors, not because the referral touchpoint itself converts
- **Affiliates cuts are model-confirmed:** the negative coefficient holds across all three model types after controlling for all other session features; this is not a volume problem but a quality problem
""")
