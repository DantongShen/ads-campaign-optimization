import streamlit as st
from pathlib import Path

IMG = Path(__file__).parent.parent.parent / "images"

st.set_page_config(page_title="Funnel Analysis", layout="wide")
st.title("Funnel Analysis")
st.markdown("86% of sessions never reach a product page. This page maps step-by-step drop-off from session entry to completed purchase, then slices the funnel by device, channel, country, visitor type, and time to pinpoint where the friction concentrates and which segments are most affected.")

st.markdown("---")

st.subheader("Overall Funnel")
_, col, _ = st.columns([1, 3, 1])
with col:
    st.image(str(IMG / "funnel_overall.png"), use_container_width=True)
st.markdown("""
- 86% of sessions never reach a product page; the biggest loss is at discovery, not checkout
- Only 1.30% of all sessions result in a purchase
- Checkout friction concentrates at Payment and Review, not the final confirm step
""")

st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["By Device", "By Channel", "By Country", "By Visitor Type", "By Time"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.image(str(IMG / "funnel_by_device.png"), use_container_width=True)
    with col2:
        st.image(str(IMG / "funnel_device_dropoff.png"), use_container_width=True)
    st.markdown("""
    - Mobile converts at 4x lower rate than desktop; drop-off starts from the first funnel step, not just checkout
    - Tablet sits between desktop and mobile at every stage
    """)

with tab2:
    _, col, _ = st.columns([1, 3, 1])
    with col:
        st.image(str(IMG / "funnel_by_channel_line.png"), use_container_width=True)
    st.image(str(IMG / "funnel_channel_dropoff.png"), use_container_width=True)
    st.markdown("""
    - Referral converts best because it enters the funnel deeper and drops off less at each step
    - Social drives high volume but 98% of sessions never click into a product
    """)

with tab3:
    st.image(str(IMG / "funnel_by_country.png"), use_container_width=True)
    st.markdown("""
    - US converts at 28x the rate of Rest of World
    - International users who reach checkout drop off at 89% before completing, suggesting shipping restrictions or unsupported payment methods
    """)

with tab4:
    st.image(str(IMG / "funnel_by_visitor_type.png"), use_container_width=True)
    st.markdown("""
    - Returning visitors are 22% of sessions but 61% of purchases, converting at 6x the rate of new visitors
    - Their drop-off rate declines at every funnel step
    """)

with tab5:
    col1, col2 = st.columns(2)
    with col1:
        st.image(str(IMG / "funnel_by_dow.png"), caption="By day of week", use_container_width=True)
    with col2:
        st.image(str(IMG / "funnel_by_hour.png"), caption="By hour of day", use_container_width=True)
    st.markdown("""
    - Best time to convert: Monday and Friday, 10 AM to 2 PM Pacific
    - Weekday purchase intent is nearly double weekend rates
    """)

st.markdown("---")

st.subheader("Checkout Steps")
_, col, _ = st.columns([1, 3, 1])
with col:
    st.image(str(IMG / "funnel_checkout_steps.png"), use_container_width=True)
st.markdown("""
- Drop-off concentrates at the Payment step (entering card details) and the Review step
- Almost no one abandons after reaching the final confirm step
""")

st.markdown("---")

st.subheader("Recommendations")
st.markdown("""
- **Run the mobile navigation A/B test first:** the session-to-product-page gap is the largest single drop-off and affects all downstream metrics; this is the highest-leverage intervention available (see Experiment Design page for the full test plan)
- **Address checkout Payment and Review steps as a follow-on:** once the top-of-funnel mobile gap is closed, checkout friction becomes the next largest opportunity; focus on reducing form complexity at payment and clarifying the order summary at review
- **Prioritize returning visitor retention:** returning visitors convert at 6x the rate of new visitors; programs that bring users back (email, retargeting) have a higher expected return than acquiring new traffic
- **Do not invest in international conversion without infrastructure:** US converts at 28x the rest of the world; the 89% international checkout drop-off signals missing payment methods or shipping options, not a marketing problem
""")

