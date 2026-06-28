import streamlit as st
from pathlib import Path

IMG = Path(__file__).parent.parent.parent / "images"

st.set_page_config(page_title="EDA", layout="wide")
st.title("Exploratory Data Analysis")
st.caption("User behavior, purchase patterns, geography, and device breakdown across the full dataset period.")

st.markdown("---")

st.subheader("Pageview Depth")
st.markdown("""
Pageview depth is the strongest behavioral signal in the dataset. Purchasers and non-purchasers have almost non-overlapping distributions.
""")
_, col, _ = st.columns([1, 3, 1])
with col:
    st.image(str(IMG / "pageviews_percentile.png"), use_container_width=True)
st.image(str(IMG / "pageviews_distribution_comparison.png"), use_container_width=True)
st.markdown("""
- Median purchaser views 37 pages vs 2 for non-purchasers; the distributions barely overlap
- ~10 pageviews is a natural threshold: below it non-purchasers dominate, above it purchasers become the majority
- 75% of non-purchasers view 4 or fewer pages; purchasers spread widely from 10 to 100+
""")

st.markdown("---")

st.subheader("Purchase Behavior")
col1, col2 = st.columns(2)
with col1:
    st.image(str(IMG / "transactions_per_user.png"), use_container_width=True)
with col2:
    st.image(str(IMG / "spend_per_order_dist.png"), use_container_width=True)
st.markdown("""
- 88% of buyers purchase only once; only ~4% make 3 or more purchases; repeat buying is rare
- Most orders fall between \$25 and \$75, accounting for ~43% of all purchasing sessions
- Median spend (\$56) vs mean (\$155) gap is large; a small number of high-spend orders inflate the average significantly
- Long tail of high-spend orders likely represents corporate or bulk buyers
""")

st.markdown("---")

st.subheader("Browser and Device")
st.image(str(IMG / "browser_transactions.png"), use_container_width=True)
st.markdown("""
- Chrome leads on both volume (10,924 transactions) and conversion rate (1.76%), far ahead of every other browser
- Safari has high volume but low conversion (0.43%), the lowest among desktop browsers
- Mobile browsers barely convert: Safari in-app at 0.18% and Android Webview at 0.08%; the store is effectively a desktop-first experience
- Firefox and Internet Explorer convert above Safari despite lower volume, suggesting higher purchase intent among their users
""")

st.markdown("---")

st.subheader("Traffic Source Engagement")
_, col, _ = st.columns([1, 3, 1])
with col:
    st.image(str(IMG / "real_bounce_rate.png"), use_container_width=True)
st.markdown("""
- Direct traffic (41.8% bounce) has the best combination of volume and engagement
- YouTube (66% bounce) drives reach but almost no purchase intent; high volume, low quality
- `analytics.google.com` (52.3% bounce, 0 transactions across 16K sessions) is internal Google traffic, excluded from all channel analyses
- `sites.google.com` and `siliconvalley.about.com` have the lowest bounce rates among referral sources, reflecting curated high-intent links
""")

st.markdown("---")

st.subheader("Geography")
st.image(str(IMG / "country_performance.png"), use_container_width=True)
st.markdown("""
- US generates 94% of transactions from 40% of sessions at a 3.14% conversion rate, far ahead of every other market
- Canada is the only other market with real traction: 0.77% conversion and \$175 AOV
- Large markets with near-zero conversion: India (51K sessions), Vietnam (24K sessions), UK (37K sessions) all convert below 0.16%
- Japan's \$424 AOV is misleading: 3 of 17 transactions account for 89% of Japan revenue; median spend is ~\$50
- Outside the US and Canada, every country converts below 0.15%; international traffic is largely non-converting reach
""")
