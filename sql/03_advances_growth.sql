-- ========================================================================
-- Q3: ADVANCES (LOAN BOOK) GROWTH — FY20 vs FY25
-- Business question: Which banks actually grew their loan book the most
-- over the 6-year horizon? Compound annual growth rate (CAGR) is the
-- right metric, but we can approximate it with the % change FY20→FY25.
-- ========================================================================

WITH endpoints AS (
    SELECT
        bank_name,
        bank_type,
        MAX(CASE WHEN financial_year = 'FY20' THEN advances_cr END) AS adv_fy20,
        MAX(CASE WHEN financial_year = 'FY25' THEN advances_cr END) AS adv_fy25
    FROM bank_financials
    GROUP BY bank_name, bank_type
)
SELECT
    bank_name,
    bank_type,
    adv_fy20,
    adv_fy25,
    ROUND(adv_fy25 - adv_fy20, 0) AS absolute_growth_cr,
    ROUND(100.0 * (adv_fy25 - adv_fy20) / NULLIF(adv_fy20, 0), 1) AS growth_pct,
    -- 5-year CAGR = (end/start)^(1/5) - 1
    ROUND(100.0 * ((POWER(adv_fy25 * 1.0 / NULLIF(adv_fy20, 0), 0.2)) - 1), 1) AS cagr_pct
FROM endpoints
ORDER BY growth_pct DESC;
