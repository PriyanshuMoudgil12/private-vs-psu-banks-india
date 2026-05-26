-- ========================================================================
-- Q2: ASSET QUALITY — GROSS NPAs
-- Business question: How "bad" is each group's loan book? Has the PSU
-- clean-up actually closed the gap with private peers?
-- Metric: Gross NPA % (lower is better).
-- ========================================================================

SELECT
    financial_year,
    ROUND(AVG(CASE WHEN bank_type = 'Private' THEN gross_npa_pct END), 2) AS private_gnpa_pct,
    ROUND(AVG(CASE WHEN bank_type = 'PSU'     THEN gross_npa_pct END), 2) AS psu_gnpa_pct,
    ROUND(
        AVG(CASE WHEN bank_type = 'PSU'     THEN gross_npa_pct END)
      - AVG(CASE WHEN bank_type = 'Private' THEN gross_npa_pct END),
    2) AS psu_excess_gnpa_pp
FROM bank_financials
GROUP BY financial_year
ORDER BY financial_year;
