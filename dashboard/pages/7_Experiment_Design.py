import streamlit as st
from pathlib import Path

IMG = Path(__file__).parent.parent.parent / "images"

st.set_page_config(page_title="Experiment Design", layout="wide")
st.title("Experiment Design: Mobile Navigation and Discovery")

st.markdown("""
The funnel analysis identified mobile session-to-product-page rate as the highest-leverage bottleneck in the purchase funnel.
This page documents the full A/B test design for a mobile homepage navigation intervention,
including sample size requirements, decision rules, pre-launch checks, and post-launch analysis guidance.
""")

st.markdown("---")

st.subheader("Motivation")
_, col, _ = st.columns([1, 3, 1])
with col:
    st.image(str(IMG / "funnel_by_device.png"), use_container_width=True)
st.markdown("""
Funnel analysis showed mobile converts at 4x lower than desktop. The drop-off starts from the very first step: mobile product page view rate is 12.38% vs 14.45% on desktop. The intervention targets this first bottleneck, not checkout, where friction also exists but is secondary.
""")

st.markdown("---")

st.subheader("Experiment Design")
st.markdown("""
| Parameter | Value |
|---|---|
| Intervention | Mobile homepage navigation redesign |
| Unit | Session (smartphone only, tablet excluded) |
| Split | 50/50 control / treatment |
| Primary metric | Mobile product page view rate |
| Secondary metric | Mobile revenue per session |
| Guardrail metrics | Desktop conversion rate, desktop revenue per session |
| MDE | 20% relative lift |
| Significance level | 0.05 |
| Statistical power | 0.80 |
""")

st.subheader("Key Outputs")
st.markdown("""
| Output | Value |
|---|---|
| Baseline product page view rate | 12.38% |
| Target rate at 20% lift | 14.86% |
| Required sessions per group | 2,372 |
| Total sessions required | 4,744 |
| Avg daily mobile sessions | 570 |
| Recommended duration | 2 weeks |
""")

st.markdown("---")

st.subheader("Sample Size Sensitivity")
st.image(str(IMG / "sensitivity_analysis.png"), use_container_width=True)
st.markdown("""
- 20% MDE at 9 raw days is the practical sweet spot, rounded to 2 weeks to cover a full weekday/weekend cycle
- Detecting a 10% lift would require 33 days (over 4 weeks), introducing seasonal noise
- Going from 10% to 20% MDE cuts required sessions by 74% (18,248 to 4,744)
""")

st.markdown("---")

st.subheader("Decision Rules")
st.markdown("""
- **Ship if:** p-value < 0.05 on primary metric and guardrail metrics show no regression
- **Hold if:** SRM detected (chi-squared p < 0.05 on the 50/50 split), or experiment ran fewer than one full week
- **Primary up, revenue per session flat:** more users browsed but did not buy; downstream funnel may need a separate intervention
- **Primary flat:** navigation redesign did not change user behaviour; revisit the intervention
""")

st.markdown("---")

st.subheader("Pre-launch Checks")
st.markdown("""
**Sample Ratio Mismatch (SRM)**

In a 50/50 split, control and treatment should receive roughly equal session counts. Run a chi-squared test after the first 24 to 48 hours. If p < 0.05, the randomisation is broken and results should be discarded.

**Novelty effect**

Segment results by new vs returning visitors. If returning visitors drive all the lift and new visitors show nothing, the effect may be novelty-driven and could decay after rollout.
""")

st.markdown("---")

st.subheader("Post-Launch Analysis")
st.markdown("""
After the experiment concludes, run the following analyses before making a ship or no-ship decision:

**Segment breakdown**
- Split results by new vs returning visitors: novelty effects concentrate in returning visitors in the first week; if their lift decays by week two, do not attribute it to the design
- Split by channel: Organic and Direct users are the core audience; if lift only shows in Paid Search or Social, the design may only help high-intent sessions
- Split by US vs international: US is 94% of transactions; a positive overall result driven only by international sessions may not translate to revenue

**Novelty effect check**
- Plot the primary metric by day for each group; a genuine effect is stable or growing across both weeks; a novelty spike that decays in the second week warrants holding the decision

**Next steps if significant**
- Roll out to 100% of mobile sessions and monitor for two additional weeks to confirm the lift holds at scale
- Move to the next bottleneck: checkout Payment and Review step drop-off (separate experiment)

**Next steps if not significant**
- The navigation change did not affect how users discover products; the bottleneck may be deeper: product page quality (images, descriptions, search) rather than navigation
- Revisit the intervention hypothesis before designing a follow-on test
""")

st.markdown("---")

st.subheader("Recommendations")
st.markdown("""
- **Run the experiment for the full 2 weeks:** cutting it short risks missing a full weekday/weekend cycle, which matters given weekday purchase intent is nearly double weekend rates
- **Check SRM in the first 24 to 48 hours:** do not wait until the end; a broken randomisation wastes the entire experiment window
- **If the primary metric lifts but revenue per session stays flat:** more users are browsing but not buying; the navigation change worked but the downstream product or checkout experience needs a separate intervention
- **Segment by new vs returning visitors throughout:** novelty effects are most likely to show up in returning visitors; if the lift is driven entirely by returning users in the first few days, monitor whether it sustains before deciding to ship
""")
