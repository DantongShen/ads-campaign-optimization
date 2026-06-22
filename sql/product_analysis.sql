-- product_analysis.sql
-- All SQL queries from 04_product_analysis.ipynb
-- Standard filters applied throughout:
--   - trafficSource.source != 'analytics.google.com'  (exclude internal Google traffic)
--   - product.isImpression IS NULL OR product.isImpression = FALSE  (exclude list impressions)
--   - product.productRevenue IS NOT NULL  (revenue queries only: ensure product was purchased)


-- Section 2a: Column Overview (single-day sample, action_type 2/3/6)
-- variable: query_product_cols
SELECT * FROM (
    SELECT hits.eCommerceAction.action_type, product.isImpression,
           product.v2ProductName, product.v2ProductCategory,
           product.productSKU, product.productPrice / 1000000 AS price_usd,
           product.productRevenue / 1000000 AS revenue_usd, product.productQuantity
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_20170101`,
    UNNEST(hits) AS hits, UNNEST(hits.product) AS product
    WHERE hits.eCommerceAction.action_type = '2' LIMIT 3
)
UNION ALL
SELECT * FROM (
    SELECT hits.eCommerceAction.action_type, product.isImpression,
           product.v2ProductName, product.v2ProductCategory,
           product.productSKU, product.productPrice / 1000000 AS price_usd,
           product.productRevenue / 1000000 AS revenue_usd, product.productQuantity
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_20170101`,
    UNNEST(hits) AS hits, UNNEST(hits.product) AS product
    WHERE hits.eCommerceAction.action_type = '3' LIMIT 3
)
UNION ALL
SELECT * FROM (
    SELECT hits.eCommerceAction.action_type, product.isImpression,
           product.v2ProductName, product.v2ProductCategory,
           product.productSKU, product.productPrice / 1000000 AS price_usd,
           product.productRevenue / 1000000 AS revenue_usd, product.productQuantity
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_20170101`,
    UNNEST(hits) AS hits, UNNEST(hits.product) AS product
    WHERE hits.eCommerceAction.action_type = '6' LIMIT 3
)
ORDER BY action_type


-- Section 2a: Data Scope - unique SKUs, names, categories, purchase rows
-- variable: query_product_scope
SELECT
    COUNT(DISTINCT product.productSKU) AS unique_skus,
    COUNT(DISTINCT product.v2ProductName) AS unique_names,
    COUNT(DISTINCT product.v2ProductCategory) AS unique_categories,
    COUNTIF(hits.eCommerceAction.action_type = '6'
        AND (product.isImpression IS NULL OR product.isImpression = FALSE)
        AND product.productRevenue IS NOT NULL) AS purchase_product_rows
FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
UNNEST(hits) AS hits,
UNNEST(hits.product) AS product


-- Section 2a: Category Tagging Bug - sample rows with bad category
-- variable: query_bad_category_sample
SELECT
    hits.eCommerceAction.action_type,
    product.v2ProductName,
    product.v2ProductCategory,
    product.productSKU,
    product.productPrice / 1000000 AS price_usd
FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
UNNEST(hits) AS hits,
UNNEST(hits.product) AS product
WHERE (product.isImpression IS NULL OR product.isImpression = FALSE)
  AND product.v2ProductCategory = '${escCatTitle}'
LIMIT 5


-- Section 2a: Category Tagging Bug - scale of the problem
-- variable: query_bad_category
SELECT
    COUNT(*)                              AS total_rows,
    COUNT(DISTINCT product.productSKU)    AS affected_skus,
    COUNT(DISTINCT product.v2ProductName) AS affected_products
FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
UNNEST(hits) AS hits,
UNNEST(hits.product) AS product
WHERE (product.isImpression IS NULL OR product.isImpression = FALSE)
  AND product.v2ProductCategory = '${escCatTitle}'


-- Section 2a: Canonical category map - most frequent valid category per product name
-- variable: query_product_category_map
WITH category_counts AS (
    SELECT
        product.v2ProductName,
        product.v2ProductCategory AS category,
        COUNT(*) AS row_count
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
    UNNEST(hits) AS hits,
    UNNEST(hits.product) AS product
    WHERE (product.isImpression IS NULL OR product.isImpression = FALSE)
        AND product.v2ProductCategory IS NOT NULL
        AND product.v2ProductCategory != '${escCatTitle}'
    GROUP BY product.v2ProductName, product.v2ProductCategory
),
ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY v2ProductName ORDER BY row_count DESC) AS rn
    FROM category_counts
)
SELECT v2ProductName, category AS canonical_category, row_count
FROM ranked
WHERE rn = 1
ORDER BY v2ProductName


-- Section 2a: Resolution check - how many bad-category products can be resolved
-- variable: query_resolution_check
WITH bad_products AS (
    SELECT
        product.v2ProductName,
        COUNT(*) AS bad_rows
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
    UNNEST(hits) AS hits,
    UNNEST(hits.product) AS product
    WHERE (product.isImpression IS NULL OR product.isImpression = FALSE)
      AND product.v2ProductCategory = '${escCatTitle}'
    GROUP BY product.v2ProductName
),
category_counts AS (
    SELECT
        product.v2ProductName,
        product.v2ProductCategory,
        COUNT(*) AS cnt
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
    UNNEST(hits) AS hits,
    UNNEST(hits.product) AS product
    WHERE (product.isImpression IS NULL OR product.isImpression = FALSE)
      AND product.v2ProductCategory IS NOT NULL
      AND product.v2ProductCategory != '${escCatTitle}'
    GROUP BY product.v2ProductName, product.v2ProductCategory
),
canonical AS (
    SELECT
        v2ProductName,
        ARRAY_AGG(v2ProductCategory ORDER BY cnt DESC LIMIT 1)[OFFSET(0)] AS resolved_category
    FROM category_counts
    GROUP BY v2ProductName
)
SELECT
    b.v2ProductName,
    b.bad_rows,
    c.resolved_category
FROM bad_products b
LEFT JOIN canonical c USING (v2ProductName)
ORDER BY b.bad_rows DESC


-- Section 3: Top Products by Revenue & Transactions
-- variable: query_top_products
SELECT
    product.v2ProductName AS product_name,
    ROUND(SUM(product.productRevenue / 1000000), 2) AS total_revenue,
    COUNT(*) AS purchase_rows,
    SUM(product.productQuantity) AS total_units
FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
UNNEST(hits) AS hits,
UNNEST(hits.product) AS product
WHERE trafficSource.source != 'analytics.google.com'
    AND hits.eCommerceAction.action_type = '6'
    AND (product.isImpression IS NULL OR product.isImpression = FALSE)
    AND product.productRevenue IS NOT NULL
GROUP BY product_name
ORDER BY total_revenue DESC


-- Section 6: Product Page Conversion (Detail View -> Add to Cart)
-- variable: query_view_to_cart
-- Session-level: both CTEs group by (fullVisitorId, visitId, product_name) before joining
-- so numerator and denominator always come from the same sessions
WITH detail_views AS (
    SELECT
        fullVisitorId,
        visitId,
        product.v2ProductName AS product_name
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
    UNNEST(hits) AS hits,
    UNNEST(hits.product) AS product
    WHERE trafficSource.source != 'analytics.google.com'
        AND hits.eCommerceAction.action_type = '2'
        AND (product.isImpression IS NULL OR product.isImpression = FALSE)
    GROUP BY fullVisitorId, visitId, product_name
),
add_to_carts AS (
    SELECT
        fullVisitorId,
        visitId,
        product.v2ProductName AS product_name
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
    UNNEST(hits) AS hits,
    UNNEST(hits.product) AS product
    WHERE trafficSource.source != 'analytics.google.com'
        AND hits.eCommerceAction.action_type = '3'
        AND (product.isImpression IS NULL OR product.isImpression = FALSE)
    GROUP BY fullVisitorId, visitId, product_name
)
SELECT
    d.product_name,
    COUNT(*)         AS sessions_viewed,
    COUNT(a.visitId) AS sessions_added_to_cart,
    ROUND(SAFE_DIVIDE(COUNT(a.visitId), COUNT(*)) * 100, 1) AS view_to_cart_pct
FROM detail_views d
LEFT JOIN add_to_carts a USING (fullVisitorId, visitId, product_name)
GROUP BY d.product_name
ORDER BY sessions_viewed DESC


-- Section 7: Cart-to-Purchase Conversion by Product (Add to Cart -> Purchase)
-- variable: query_cart_to_purchase
-- Session-level: same CTE pattern as Section 6
WITH add_to_carts AS (
    SELECT
        fullVisitorId,
        visitId,
        product.v2ProductName AS product_name
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
    UNNEST(hits) AS hits,
    UNNEST(hits.product) AS product
    WHERE trafficSource.source != 'analytics.google.com'
        AND hits.eCommerceAction.action_type = '3'
        AND (product.isImpression IS NULL OR product.isImpression = FALSE)
    GROUP BY fullVisitorId, visitId, product_name
),
purchases AS (
    SELECT
        fullVisitorId,
        visitId,
        product.v2ProductName AS product_name
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
    UNNEST(hits) AS hits,
    UNNEST(hits.product) AS product
    WHERE trafficSource.source != 'analytics.google.com'
        AND hits.eCommerceAction.action_type = '6'
        AND (product.isImpression IS NULL OR product.isImpression = FALSE)
        AND product.productRevenue IS NOT NULL
    GROUP BY fullVisitorId, visitId, product_name
)
SELECT
    a.product_name,
    COUNT(*)          AS sessions_added_to_cart,
    COUNT(p.visitId)  AS sessions_purchased,
    ROUND(SAFE_DIVIDE(COUNT(p.visitId),       COUNT(*)) * 100, 1) AS cart_to_purchase_pct,
    ROUND(100 - SAFE_DIVIDE(COUNT(p.visitId), COUNT(*)) * 100, 1) AS abandonment_pct
FROM add_to_carts a
LEFT JOIN purchases p USING (fullVisitorId, visitId, product_name)
GROUP BY a.product_name
ORDER BY sessions_added_to_cart DESC


-- Section 9: Revenue per Detail-View Session
-- variable: query_rev_per_view
-- Session-level: joins detail views with purchase revenue on (fullVisitorId, visitId, product_name)
-- so only revenue from sessions that also viewed the product detail page is counted
-- HAVING COUNT(*) >= 50 filters out low-sample products
WITH detail_views AS (
    SELECT
        fullVisitorId,
        visitId,
        product.v2ProductName AS product_name
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
    UNNEST(hits) AS hits,
    UNNEST(hits.product) AS product
    WHERE trafficSource.source != 'analytics.google.com'
        AND hits.eCommerceAction.action_type = '2'
        AND (product.isImpression IS NULL OR product.isImpression = FALSE)
    GROUP BY fullVisitorId, visitId, product_name
),
purchase_revenue AS (
    SELECT
        fullVisitorId,
        visitId,
        product.v2ProductName AS product_name,
        SUM(product.productRevenue / 1000000) AS session_revenue
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
    UNNEST(hits) AS hits,
    UNNEST(hits.product) AS product
    WHERE trafficSource.source != 'analytics.google.com'
        AND hits.eCommerceAction.action_type = '6'
        AND (product.isImpression IS NULL OR product.isImpression = FALSE)
        AND product.productRevenue IS NOT NULL
    GROUP BY fullVisitorId, visitId, product_name
)
SELECT
    d.product_name,
    COUNT(*)                                                        AS sessions_with_detail_view,
    COUNT(p.visitId)                                                AS sessions_that_purchased,
    ROUND(SUM(COALESCE(p.session_revenue, 0)), 2)                   AS revenue_from_detail_view_sessions,
    ROUND(SAFE_DIVIDE(SUM(COALESCE(p.session_revenue, 0)), COUNT(*)), 2) AS revenue_per_detail_view
FROM detail_views d
LEFT JOIN purchase_revenue p USING (fullVisitorId, visitId, product_name)
GROUP BY d.product_name
HAVING COUNT(*) >= 50
ORDER BY revenue_per_detail_view DESC
