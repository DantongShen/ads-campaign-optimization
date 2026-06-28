import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="E-commerce Analytics",
    page_icon=":bar_chart:",
    layout="wide",
)

st.title("End-to-End E-commerce Analytics and Revenue Modeling")
st.markdown(
    '<p style="font-size: 0.875rem; color: white;">Google Analytics Sample Ecommerce Dataset, Aug 2016 to Aug 2017 &nbsp;|&nbsp; <a href="https://github.com/DantongShen/ecommerce-analytics-ml" style="color: white;">GitHub</a></p>',
    unsafe_allow_html=True,
)

st.markdown("---")

st.subheader("Background")
st.markdown("""
The Google Merchandise Store (store.google.com) sells branded physical merchandise online.
One year of its Google Analytics data (Aug 2016 to Aug 2017, ~900K sessions) has been made public for analysis.
This project uses that dataset to evaluate channel performance, diagnose funnel drop-off, and produce data-driven recommendations for budget allocation and conversion improvement.
""")

st.markdown("---")

st.subheader("Objectives")
st.markdown("""
1. **Channel quality:** identify which channels drive real revenue, not just traffic volume
2. **Funnel diagnosis:** find where users drop off and quantify the highest-leverage UX fix
3. **Budget reallocation:** model which controllable channels should receive more or less traffic as a directional proxy for budget allocation (dollar-level optimization is out of scope; spend data is not available)
4. **Mobile conversion gap:** assess whether underperformance is an audience problem or a UX problem
5. **Purchase prediction:** build session-level models to quantify which features drive conversion probability
6. **Experiment design:** design an A/B test targeting the highest-impact funnel bottleneck identified in the analysis
""")

st.markdown("---")

st.subheader("Dataset Statistics")
st.markdown("""
**Source:** [Google Analytics Sample Dataset](https://console.cloud.google.com/marketplace/product/obfuscated-ga360-data/obfuscated-ga360-data) | **Schema:** [GA BigQuery Export Schema](https://support.google.com/analytics/answer/3437719?hl=en)

Each row is one session. Nested fields require `UNNEST`. Monetary values are stored in micros (divide by 1,000,000 for USD).
""")
stats = {
    "Metric": [
        "Total sessions", "Unique visitors", "Avg time on site",
        "Avg pageviews per session", "Total transactions",
        "Total revenue", "Conversion rate",
    ],
    "Value": [
        "903,653", "714,167", "4.4 min",
        "3.8", "12,115",
        "$1,780,149", "1.34%",
    ],
}
_, col, _ = st.columns([1, 2, 1])
with col:
    st.dataframe(pd.DataFrame(stats), hide_index=True, use_container_width=True)

st.markdown("---")

st.subheader("Key Findings")

st.markdown("**Traffic and Channel**")
st.markdown("""
- US generates 94% of transactions from 40% of sessions; Canada is the only other converting market
- Referral ranks 4th in sessions but converts at 6.25% with \$718K revenue; Social drives 226K sessions but only \$8K revenue (0.06%)
- Affiliates generated \$654 for the full year; both are confirmed reallocation candidates
- Mobile browsers convert below 0.2%; Chrome at 1.76% vs Safari at 0.43%
""")

st.markdown("**Funnel**")
st.markdown("""
- 86% of sessions never reach a product page; the bottleneck is discovery, not checkout
- Mobile converts at 4x lower rate than desktop; drop-off starts at the very first funnel step
- Returning visitors are 22% of sessions but 61% of purchases, converting at 6x the rate of new visitors
- US converts at 28x the rate of Rest of World; international users who reach checkout drop off at 89%
""")

st.markdown("**Products**")
st.markdown("""
- Top 20% of products account for 69.4% of revenue; bottom 50% contribute only 7.5%
- Apparel is 39.3% of revenue; Office leads in volume (bulk orders, likely corporate gifting)
- Bags and Electronics have a view-to-cart problem (~18%); Accessories convert into the cart but get abandoned
- Google brand converts at 2x YouTube's rate on matched products, indicating brand-driven pricing power
""")

st.markdown("**Budget Optimization**")
st.markdown("""
- Social and Affiliates hit the reallocation floor in every scenario; the most robust finding in the model
- Referral log revenue coefficient is ~13x Paid Search; it is the highest-efficiency controllable channel
- Moderate rebalance (S3): halve Social and Affiliates, double Referral, grow Paid Search and Display 50%; projects +\$51K vs baseline
- Growing Referral means more acquisition touchpoints, not same-session conversions; most of its revenue is last-non-direct-click attributed
""")

st.markdown("**Purchase Prediction**")
st.markdown("""
- All three models reach AUC 0.98+: Logistic Regression 0.9828, Random Forest 0.9860, Gradient Boosting 0.9863
- Top predictors: `is_us`, `pageviews`, `is_returning`; channel features are secondary once visitor behavior is known
- `ch_Referral` near-zero coefficient after controlling for `is_returning` confirms the attribution finding: Referral's conversion rate is returning visitor behavior, not a channel effect
- `ch_Affiliates` is the strongest negative predictor; consistent with the reallocation recommendation
""")

st.markdown("**Experiment Design**")
st.markdown("""
- Target: mobile homepage navigation redesign, addressing the first funnel bottleneck (session to product page)
- Baseline mobile product page view rate: 12.38%; target at 20% MDE: 14.86%
- Required: 2,372 sessions per group, estimated duration 2 weeks at 570 avg daily mobile sessions
- Guardrail metrics: desktop conversion rate and desktop revenue per session (should be unchanged by a mobile-only intervention)
""")

st.markdown("---")

st.subheader("Recommendations")
st.markdown("""
- **Run the mobile navigation A/B test:** the session-to-product-page gap is the largest single funnel loss; 86% of sessions never reach a product page and mobile is disproportionately worse; the experiment is fully designed and ready to execute
- **Reallocate Social and Affiliates to Referral acquisition touchpoints:** Social at 0.06% conversion and Affiliates at \$654 annual revenue cannot justify meaningful spend; Referral is the highest-efficiency channel at ~13x the Paid Search revenue coefficient; growing it means more partnerships and content placements, not simply increasing spend
- **Prioritize returning visitor retention:** returning visitors are 22% of sessions but 61% of purchases at 6x the conversion rate; email, retargeting, and loyalty programs targeting returning users have a higher expected return than broad new-user acquisition
- **Direct incremental traffic to the top ~50 products:** these drive half of all revenue; paid or referral traffic pointed at high-yield product pages is more efficient than broad category campaigns
- **Fix Bags and Electronics product pages:** both categories have high traffic but only ~18% view-to-cart rates; stronger imagery, clearer specs, and more prominent CTAs are the likely levers; Accessories add to cart at 41% but abandon at 78%, suggesting checkout reminder or bundling opportunities
- **Leverage Google brand pricing power:** Google-branded products convert at 2x YouTube equivalents even at higher price points; expanding the Google-branded assortment or increasing its visibility in navigation has a data-supported return
- **Use model probability scores for session targeting:** purchase prediction models reach AUC 0.98+; rank sessions by predicted probability to prioritize US returning visitors with 10+ pageviews for retargeting or personalization; avoid binary thresholds at a 1.30% base rate
- **Address checkout Payment and Review friction as a follow-on:** once the top-of-funnel mobile gap is closed, checkout becomes the next highest-leverage opportunity; these two steps have the highest in-checkout drop-off rate
""")
