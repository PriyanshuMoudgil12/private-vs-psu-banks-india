-- ========================================================================
-- Q1: PROFITABILITY GAP
-- Business question: How much more profitable per rupee of assets are
-- private banks than PSU banks? Has the gap widened or closed since FY20?
-- Metric: ROA (Return on Assets) — net_profit / total_assets, in %.
-- ========================================================================

SELECT
    financial_year,
    ROUND(AVG(CASE WHEN bank_type = 'Private' THEN roa_pct END), 2) AS private_roa_pct,
    ROUND(AVG(CASE WHEN bank_type = 'PSU'     THEN roa_pct END), 2) AS psu_roa_pct,
    ROUND(
        AVG(CASE WHEN bank_type = 'Private' THEN roa_pct END)
      - AVG(CASE WHEN bank_type = 'PSU'     THEN roa_pct END),
    2) AS roa_gap_pp
FROM bank_financials
GROUP BY financial_year
ORDER BY financial_year;
