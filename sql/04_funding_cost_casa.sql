-- ========================================================================
-- Q4: FUNDING ADVANTAGE — CASA RATIO
-- Business question: CASA (Current + Savings deposits) is the cheapest
-- form of bank funding. Do private banks structurally fund themselves
-- cheaper than PSUs? Where is the trend heading?
-- Metric: CASA % of deposits (higher is better — cheaper liabilities).
-- ========================================================================

SELECT
    financial_year,
    ROUND(AVG(CASE WHEN bank_type = 'Private' THEN casa_pct END), 2) AS private_casa_pct,
    ROUND(AVG(CASE WHEN bank_type = 'PSU'     THEN casa_pct END), 2) AS psu_casa_pct,
    ROUND(
        AVG(CASE WHEN bank_type = 'Private' THEN casa_pct END)
      - AVG(CASE WHEN bank_type = 'PSU'     THEN casa_pct END),
    2) AS private_casa_advantage_pp
FROM bank_financials
GROUP BY financial_year
ORDER BY financial_year;
