-- ========================================================================
-- Q5: SPREAD AND PRICING POWER — NET INTEREST MARGIN
-- Business question: Beyond having cheaper deposits, do private banks
-- also earn more on each rupee they lend? NIM captures the spread between
-- interest earned and interest paid.
-- Metric: NIM % (higher = better pricing power).
-- ========================================================================

SELECT
    bank_name,
    bank_type,
    ROUND(AVG(nim_pct), 2) AS avg_nim_pct,
    ROUND(MIN(nim_pct), 2) AS min_nim_pct,
    ROUND(MAX(nim_pct), 2) AS max_nim_pct
FROM bank_financials
GROUP BY bank_name, bank_type
ORDER BY bank_type, avg_nim_pct DESC;
