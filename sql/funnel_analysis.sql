-- funnel_analysis.sql
-- All SQL queries from 03_funnel_analysis.ipynb

-- Section 2: Column Overview (single-day sample)
-- variable: query_action_types
select 
    hits.type as hit_type,
    hits.eCommerceAction as action,
    hits.eCommerceAction.action_type as action_type,
    hits.eCommerceAction.option,
    hits.eCommerceAction.step,
    count(*) as hit_count
FROM `bigquery-public-data.google_analytics_sample.ga_sessions_20170101`,
UNNEST(hits) as hits
GROUP BY hit_type, action, action_type, option, step
ORDER BY CAST(action_type AS INT64), hit_count DESC


-- Section 2: Data Quality Check - Zero-Transaction Sources
-- variable: query_zero_tx_sources
SELECT
    trafficSource.source,
    COUNT(*) AS sessions,
    SUM(totals.transactions) AS transactions
FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`
GROUP BY trafficSource.source
HAVING transactions IS NULL AND sessions > 1000
ORDER BY sessions DESC


-- Section 3: Overall Funnel
-- variable: query_funnel
WITH t1 AS (
    SELECT
        fullVisitorId,
        visitId,
        MAX(IF(hits.eCommerceAction.action_type = '2', 1, 0)) AS reached_product_view,
        MAX(IF(hits.eCommerceAction.action_type = '3', 1, 0)) AS reached_add_to_cart,
        MAX(IF(hits.eCommerceAction.action_type = '5', 1, 0)) AS reached_checkout,
        MAX(IF(hits.eCommerceAction.action_type = '6', 1, 0)) AS reached_purchase
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
    UNNEST(hits) AS hits
    WHERE trafficSource.source != 'analytics.google.com'
    GROUP BY fullVisitorId, visitId
)
SELECT
    COUNT(*)                  AS total_sessions,
    SUM(reached_product_view) AS product_view,
    SUM(reached_add_to_cart)  AS add_to_cart,
    SUM(reached_checkout)     AS checkout,
    SUM(reached_purchase)     AS purchase
FROM t1


-- Section 3a: Checkout Sub-steps
-- variable: query_checkout_steps
WITH t1 AS (
    SELECT
        fullVisitorId,
        visitId,
        MAX(IF(hits.eCommerceAction.action_type = '5' AND hits.eCommerceAction.step = 1, 1, 0)) AS reached_billing,
        MAX(IF(hits.eCommerceAction.action_type = '5' AND hits.eCommerceAction.step = 2, 1, 0)) AS reached_payment,
        MAX(IF(hits.eCommerceAction.action_type = '5' AND hits.eCommerceAction.step = 3, 1, 0)) AS reached_review,
        MAX(IF(hits.eCommerceAction.action_type = '6', 1, 0)) AS reached_purchase
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
    UNNEST(hits) AS hits
    WHERE trafficSource.source != 'analytics.google.com'
      AND hits.eCommerceAction.action_type IN ('5', '6')
    GROUP BY fullVisitorId, visitId
)
SELECT
    SUM(reached_billing)  AS billing_shipping,
    SUM(reached_payment)  AS payment,
    SUM(reached_review)   AS review,
    SUM(reached_purchase) AS purchase
FROM t1
WHERE reached_billing = 1


-- Section 4: Funnel by Device
-- variable: query_funnel_device
WITH t1 AS (
    SELECT
        fullVisitorId,
        visitId,
        device.deviceCategory AS device,
        MAX(IF(hits.eCommerceAction.action_type = '2', 1, 0)) AS reached_product_view,
        MAX(IF(hits.eCommerceAction.action_type = '3', 1, 0)) AS reached_add_to_cart,
        MAX(IF(hits.eCommerceAction.action_type = '5', 1, 0)) AS reached_checkout,
        MAX(IF(hits.eCommerceAction.action_type = '6', 1, 0)) AS reached_purchase
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
    UNNEST(hits) AS hits
    WHERE trafficSource.source != 'analytics.google.com'
    GROUP BY fullVisitorId, visitId, device
)
SELECT
    device,
    COUNT(*)                  AS total_sessions,
    SUM(reached_product_view) AS product_view,
    SUM(reached_add_to_cart)  AS add_to_cart,
    SUM(reached_checkout)     AS checkout,
    SUM(reached_purchase)     AS purchase
FROM t1
GROUP BY device
ORDER BY total_sessions DESC


-- Section 5: Funnel by Channel
-- variable: query_funnel_channel
WITH t1 AS (
    SELECT
        fullVisitorId,
        visitId,
        channelGrouping,
        MAX(IF(hits.eCommerceAction.action_type = '2', 1, 0)) AS reached_product_view,
        MAX(IF(hits.eCommerceAction.action_type = '3', 1, 0)) AS reached_add_to_cart,
        MAX(IF(hits.eCommerceAction.action_type = '5', 1, 0)) AS reached_checkout,
        MAX(IF(hits.eCommerceAction.action_type = '6', 1, 0)) AS reached_purchase
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
    UNNEST(hits) AS hits
    WHERE trafficSource.source != 'analytics.google.com'
    GROUP BY fullVisitorId, visitId, channelGrouping
)
SELECT
    channelGrouping,
    COUNT(*)                  AS total_sessions,
    SUM(reached_product_view) AS product_view,
    SUM(reached_add_to_cart)  AS add_to_cart,
    SUM(reached_checkout)     AS checkout,
    SUM(reached_purchase)     AS purchase
FROM t1
GROUP BY channelGrouping
ORDER BY total_sessions DESC


-- Section 6: Funnel by Country
-- variable: query_funnel_country
WITH t1 AS (
    SELECT
        fullVisitorId,
        visitId,
        CASE WHEN geoNetwork.country = 'United States' THEN 'United States'
             ELSE 'Rest of World' END AS region,
        MAX(IF(hits.eCommerceAction.action_type = '2', 1, 0)) AS reached_product_view,
        MAX(IF(hits.eCommerceAction.action_type = '3', 1, 0)) AS reached_add_to_cart,
        MAX(IF(hits.eCommerceAction.action_type = '5', 1, 0)) AS reached_checkout,
        MAX(IF(hits.eCommerceAction.action_type = '6', 1, 0)) AS reached_purchase
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
    UNNEST(hits) AS hits
    WHERE trafficSource.source != 'analytics.google.com'
    GROUP BY fullVisitorId, visitId, region
)
SELECT
    region,
    COUNT(*)                  AS total_sessions,
    SUM(reached_product_view) AS product_view,
    SUM(reached_add_to_cart)  AS add_to_cart,
    SUM(reached_checkout)     AS checkout,
    SUM(reached_purchase)     AS purchase
FROM t1
GROUP BY region
ORDER BY total_sessions DESC


-- Section 7a: Funnel by Hour of Day (US Pacific)
-- variable: query_funnel_hour
WITH t1 AS (
    SELECT
        fullVisitorId,
        visitId,
        EXTRACT(HOUR FROM DATETIME(TIMESTAMP_SECONDS(visitStartTime), 'America/Los_Angeles')) AS hour,
        MAX(IF(hits.eCommerceAction.action_type = '2', 1, 0)) AS reached_product_view,
        MAX(IF(hits.eCommerceAction.action_type = '3', 1, 0)) AS reached_add_to_cart,
        MAX(IF(hits.eCommerceAction.action_type = '5', 1, 0)) AS reached_checkout,
        MAX(IF(hits.eCommerceAction.action_type = '6', 1, 0)) AS reached_purchase
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
    UNNEST(hits) AS hits
    WHERE trafficSource.source != 'analytics.google.com'
    GROUP BY fullVisitorId, visitId, hour
)
SELECT
    hour,
    COUNT(*)                  AS total_sessions,
    SUM(reached_product_view) AS product_view,
    SUM(reached_add_to_cart)  AS add_to_cart,
    SUM(reached_checkout)     AS checkout,
    SUM(reached_purchase)     AS purchase
FROM t1
GROUP BY hour
ORDER BY hour


-- Section 7b: Funnel by Day of Week (US Pacific)
-- variable: query_funnel_dow
WITH t1 AS (
    SELECT
        fullVisitorId,
        visitId,
        FORMAT_DATE('%A', DATE(TIMESTAMP_SECONDS(visitStartTime), 'America/Los_Angeles')) AS day_of_week,
        EXTRACT(DAYOFWEEK FROM DATE(TIMESTAMP_SECONDS(visitStartTime), 'America/Los_Angeles')) AS day_num,
        MAX(IF(hits.eCommerceAction.action_type = '2', 1, 0)) AS reached_product_view,
        MAX(IF(hits.eCommerceAction.action_type = '3', 1, 0)) AS reached_add_to_cart,
        MAX(IF(hits.eCommerceAction.action_type = '5', 1, 0)) AS reached_checkout,
        MAX(IF(hits.eCommerceAction.action_type = '6', 1, 0)) AS reached_purchase
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
    UNNEST(hits) AS hits
    WHERE trafficSource.source != 'analytics.google.com'
    GROUP BY fullVisitorId, visitId, day_of_week, day_num
)
SELECT
    day_num,
    day_of_week,
    COUNT(*)                  AS total_sessions,
    SUM(reached_product_view) AS product_view,
    SUM(reached_add_to_cart)  AS add_to_cart,
    SUM(reached_checkout)     AS checkout,
    SUM(reached_purchase)     AS purchase
FROM t1
GROUP BY day_num, day_of_week
ORDER BY day_num

