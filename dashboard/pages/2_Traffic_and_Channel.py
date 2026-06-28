import streamlit as st
import pandas as pd
from pathlib import Path

IMG = Path(__file__).parent.parent.parent / "images"
DATA = Path(__file__).parent.parent.parent / "data"

st.set_page_config(page_title="Traffic & Channel", layout="wide")
st.title("Traffic and Channel Analysis")
st.markdown("Not all traffic is equal. This page breaks down session volume, revenue, and engagement by channel, tracks how the channel mix shifted month to month, and evaluates campaign-level performance to surface where budget is well spent and where it is not.")

st.markdown("---")

st.subheader("Session and Revenue by Channel")
st.image(str(IMG / "channel_performance.png"), use_container_width=True)

_, col, _ = st.columns([1, 3, 1])
with col:
    st.image(str(IMG / "channel_revenue_per_session.png"), use_container_width=True)

st.markdown("""
- Referral ranks 4th in sessions but 1st in revenue efficiency: 6.25% conversion rate and \$718K total revenue
- Social drives 226K sessions (2nd highest) but only \$8K revenue (0.06% conversion)
- Affiliates generated \$654 over the full year; both Social and Affiliates are confirmed reallocation candidates
- Direct and Organic Search are the two largest session sources; Organic converts at roughly 2x Paid Search
- Display AOV (\$857) is misleading: a handful of large dfa/cpm orders inflate the mean; excluding them, April 2017 AOV drops from \$232 to \$137
""")

st.markdown("---")

st.subheader("Channel Efficiency")
_, col, _ = st.columns([1, 3, 1])
with col:
    st.image(str(IMG / "channel_efficiency.png"), use_container_width=True)
st.markdown("The channel ranking by yield is consistent across engagement metrics (bounce rate, time on site, pages per session) and conversion metrics (conversion rate, revenue per session); Referral and Direct lead across all dimensions while Social and Affiliates trail across all dimensions.")

st.markdown("---")

st.subheader("Monthly Traffic Trend")
st.image(str(IMG / "monthly_trend.png"), use_container_width=True)
st.image(str(IMG / "sessions_per_day.png"), use_container_width=True)

st.markdown("""
- Sessions peak in Nov/Dec 2016 (holiday season) with a sharp post-holiday drop in Jan 2017
- November had the most sessions (114K) but the lowest conversion rate (0.84%); holiday traffic volume is mostly browse-and-leave behavior
- December had the highest conversion (1.83%) but one of the lowest AOVs (\$115); holiday buyers are decisive but buy cheaper items, not big-ticket purchases
""")

st.markdown("---")

st.subheader("Monthly Spend")
st.image(str(IMG / "spend_monthly.png"), use_container_width=True)
st.markdown("""
- April 2017 shows the highest AOV (\$232) and revenue per session (\$3.32), but this is driven by 11 dfa/cpm (Display) transactions averaging \$8,477 each; excluding them, April AOV drops to \$137
- Holiday months (Nov-Dec) sit below the full-year AOV average (~\$150); high conversion in December does not mean higher spend per order
- Aug 2017 covers only 1 day of data and should not be compared against other months
""")

st.markdown("---")

st.subheader("Monthly Channel Mix")
st.image(str(IMG / "channel_mix_monthly.png"), caption="Share of sessions by channel", use_container_width=True)
st.image(str(IMG / "channel_mix_monthly_abs.png"), caption="Absolute sessions by channel", use_container_width=True)

st.markdown("""
- Organic Search consistently holds the largest share of sessions throughout the year; Direct is a close second
- Referral share is small but stable; its outsized revenue contribution relative to session share is the clearest sign of channel quality difference
- Social share spikes in holiday months but does not produce a matching revenue spike, reinforcing it as a reach channel rather than a conversion channel
- Paid Search and Display remain minor in absolute volume, leaving room for reallocation if cost-per-session is favorable
""")

st.markdown("---")

st.subheader("Campaign Performance")
st.image(str(IMG / "campaign_performance.png"), use_container_width=True)
st.markdown("""
- Only 3 of 8 named campaigns generated any transactions; named campaigns account for less than 2% of total revenue (\$28K of \$1.78M)
- AW Accessories (\$15.6K revenue, \$156 AOV) and AW Dynamic Search Ads (2.27% conversion) are the only two campaigns delivering measurable value
- AW Apparel and AW Electronics are effectively dormant: 106 combined sessions and zero transactions over the full year
- Data Share Promo drove 16K affiliate sessions but only 9 transactions (0.05%); confirms the Affiliates channel failure
""")

st.markdown("---")

st.subheader("Source / Medium Breakdown")
st.markdown("""
Session and revenue breakdown by source and medium across the full dataset period. Use this to identify specific traffic sources driving outsized or underperforming revenue relative to their session volume.
Columns: `channelGrouping` (GA channel label), `source`, `medium`, `is_true_direct` (direct traffic with no referrer), `sessions`, `transactions`, `revenue`.
""")
df = pd.read_csv(DATA / "source_medium_breakdown.csv")
st.dataframe(df, hide_index=True, use_container_width=True)

st.markdown("---")

st.subheader("Recommendations")
st.markdown("""
- **Cut or floor Social and Affiliates:** Social at 0.06% conversion and Affiliates at \$654 annual revenue cannot justify meaningful budget; reallocate to higher-efficiency channels
- **Invest in Referral acquisition touchpoints:** Referral is the highest-efficiency channel at ~13x Paid Search revenue coefficient; growing it means creating more entry points (partnerships, content, backlinks), not just increasing spend
- **Investigate the mobile browser gap:** Chrome converts at 1.76% and Safari at 0.43% on the same site; this gap warrants separate UX investigation alongside the navigation A/B test
- **Treat US and Canada differently from all other markets:** US generates 94% of transactions; international traffic is largely non-converting and should not inform channel budget decisions without separate segmentation
""")

