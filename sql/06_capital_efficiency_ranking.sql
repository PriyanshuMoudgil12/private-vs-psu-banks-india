-- ========================================================================
-- Q6: CAPITAL-EFFICIENCY LEAGUE TABLE — FY25
-- Business question: For the latest year, give the CEO a single ranked
-- table that fuses size (assets) with quality (ROA, NPA, CASA) so the
-- "winners" and "laggards" are unmistakable.
-- Methodology: Rank each bank on every dimension, then average ranks.
-- ========================================================================

WITH fy25 AS (
    SELECT *
    FROM bank_financials
    WHERE financial_year = 'FY25'
),
ranked AS (
    SELECT
        bank_name,
        bank_type,
        total_assets_cr,
        net_profit_cr,
        roa_pct,
        gross_npa_pct,
        casa_pct,
        nim_pct,
        -- Lower NPA is better → ascending rank.
        RANK() OVER (ORDER BY gross_npa_pct ASC)  AS rk_npa,
        -- Higher ROA / NIM / CASA / profit is better → descending rank.
        RANK() OVER (ORDER BY roa_pct      DESC) AS rk_roa,
        RANK() OVER (ORDER BY nim_pct      DESC) AS rk_nim,
        RANK() OVER (ORDER BY casa_pct     DESC) AS rk_casa,
        RANK() OVER (ORDER BY net_profit_cr DESC) AS rk_profit
    FROM fy25
)
SELECT
    bank_name,
    bank_type,
    total_assets_cr,
    net_profit_cr,
    roa_pct,
    gross_npa_pct,
    casa_pct,
    nim_pct,
    ROUND((rk_npa + rk_roa + rk_nim + rk_casa + rk_profit) / 5.0, 2) AS avg_rank
FROM ranked
ORDER BY avg_rank ASC;
