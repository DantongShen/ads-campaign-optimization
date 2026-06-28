import streamlit as st
import pandas as pd
from pathlib import Path

IMG = Path(__file__).parent.parent.parent / "images"
DATA = Path(__file__).parent.parent.parent / "data"

st.set_page_config(page_title="Product Analysis", layout="wide")
st.title("Product Analysis")
st.markdown("Revenue is heavily concentrated: the top 20% of products account for nearly 70% of total revenue. This page examines where that concentration sits, how well different categories convert from product view to cart to purchase, and whether brand affects buying behavior on comparable products.")

st.markdown("---")

st.subheader("Revenue by Category")
st.image(str(IMG / "category_revenue.png"), use_container_width=True)

_, col, _ = st.columns([1, 3, 1])
with col:
    st.image(str(IMG / "revenue_concentration.png"), use_container_width=True)

st.markdown("""
- Apparel accounts for 39.3% of total revenue; Office leads in units sold (bulk journal/notebook orders, likely corporate gifting)
- The top 20% of products account for 69.4% of revenue; the bottom 50% contribute only 7.5%
- A manageable set of ~50 products drives half of all revenue
""")

st.markdown("---")

st.subheader("View-to-Cart Conversion")
col1, col2 = st.columns(2)
with col1:
    st.image(str(IMG / "view_to_cart_category.png"), caption="By category", use_container_width=True)
with col2:
    st.image(str(IMG / "view_to_cart_product_scatter.png"), caption="By product", use_container_width=True)

_, col, _ = st.columns([1, 3, 1])
with col:
    st.image(str(IMG / "view_to_cart_product_bar.png"), use_container_width=True)

st.markdown("""
- Bags and Electronics have a view-to-cart problem (~18%): high traffic but low add-to-cart conversion
- Accessories convert best into the cart (41%) but worst out of it (22%); impulse adds that get abandoned if no primary purchase occurs
""")

st.markdown("---")

st.subheader("Revenue per Product View")
st.markdown("*Revenue per product view = total revenue from a product divided by the number of sessions that viewed its detail page. A high value means each visit to that product page tends to generate meaningful revenue, either through a high purchase rate, a high price, or both.*")
col1, col2 = st.columns(2)
with col1:
    st.image(str(IMG / "revenue_per_view.png"), use_container_width=True)
with col2:
    st.image(str(IMG / "cart_to_purchase_product_bar.png"), use_container_width=True)

st.markdown("""
- Two drivers of high revenue per product view: high unit price and bulk buying
- High-yield products (high revenue per view) with high traffic are the most efficient targets for incremental traffic investment; sending more visitors to a page that already converts well compounds the return
""")

st.markdown("---")

st.subheader("Brand Comparison")
st.markdown("The store carries products under three in-house brands: Google, YouTube, and Android. The first chart compares overall conversion rates across all products by brand. However, brand alone conflates product type and price, so the second chart controls for this by selecting matched pairs — the same product type sold under different brands, to isolate the brand effect.")
_, col, _ = st.columns([1, 3, 1])
with col:
    st.image(str(IMG / "brand_conversion.png"), use_container_width=True)

st.markdown("The matched-pair comparison below compares cart-to-purchase rates for the same product types across brands, removing the noise from different category mixes.")
st.image(str(IMG / "brand_pairs_comparison.png"), use_container_width=True)

st.markdown("""
- Google brand has a consistent purchase conversion advantage over YouTube and Android in matched-pair comparisons
- Google cart-to-purchase exceeds YouTube in all 4 pairs, converting at 2x YouTube's rate on journals even when priced higher; the advantage holds even where Google products are priced above YouTube equivalents, suggesting brand-driven willingness to pay
""")

st.markdown("---")

st.subheader("Product Category Data")
st.markdown("""
Normalized product catalog mapping each product to a canonical category and brand. Use this to filter or drill into specific categories and brands.
Columns: `v2ProductName` (raw product name), `canonical_category` (original GA category path), `normalized_category` (cleaned label), `brand` (Google, YouTube, Android, or Other), `row_count` (number of hit-level rows for this product).
""")
df = pd.read_csv(DATA / "product_category_normalized.csv")
st.dataframe(df, hide_index=True, use_container_width=True)

st.markdown("---")

st.subheader("Recommendations")
st.markdown("""
- **Focus incremental traffic on the top ~50 products:** these drive half of all revenue; directing paid or referral traffic to high-yield product pages is more efficient than broad category campaigns
- **Investigate Bags and Electronics product pages:** both categories have high traffic but only ~18% view-to-cart rates; better product imagery, clearer sizing/specs, or stronger CTAs are likely to move the needle
- **Leverage Google brand pricing power:** Google-branded products convert at 2x the rate of YouTube equivalents even at higher price points; this suggests room to expand the Google-branded assortment or increase its visibility in navigation
- **Monitor Accessories cart abandonment:** Accessories have the highest add-to-cart rate (41%) but convert out of the cart at only 22%; these are likely impulse adds that drop off when no primary purchase is made; bundling or checkout reminders could recover some of this
""")

