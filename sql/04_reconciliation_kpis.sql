-- ============================================================================
-- Enterprise Sales & Revenue Intelligence System
-- 04_reconciliation_kpis.sql: SQL Ground-Truth KPI Reconciliation Suite
-- SRS Reference: Appendix A (KPI Definitions) & Section 10 (AC-03, AC-04)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Section 1: Executive KPI Totals (Global Fleet Baseline)
-- ----------------------------------------------------------------------------
SELECT 
    'Executive Lifetime Summary' AS Scope,
    ROUND(SUM(Quantity * UnitPrice), 2) AS GrossSales,
    ROUND(SUM(DiscountAmount), 2) AS DiscountAmount,
    ROUND(SUM(Quantity * UnitPrice - DiscountAmount), 2) AS NetSales_Revenue,
    ROUND(SUM(Quantity * UnitCost), 2) AS CostOfGoodsSold,
    ROUND(SUM(Quantity * UnitPrice - DiscountAmount) - SUM(Quantity * UnitCost), 2) AS GrossProfit,
    ROUND(
        (SUM(Quantity * UnitPrice - DiscountAmount) - SUM(Quantity * UnitCost)) * 100.0 / 
        NULLIF(SUM(Quantity * UnitPrice - DiscountAmount), 0), 2
    ) AS GrossMarginPct,
    COUNT(DISTINCT OrderID) AS DistinctOrderCount,
    SUM(Quantity) AS TotalUnitsSold,
    ROUND(
        SUM(Quantity * UnitPrice - DiscountAmount) / NULLIF(COUNT(DISTINCT OrderID), 0), 2
    ) AS AverageOrderValue_AOV
FROM FactSales;

-- ----------------------------------------------------------------------------
-- Section 2: Annual Performance Breakdown (2024 vs 2025 vs 2026)
-- ----------------------------------------------------------------------------
SELECT 
    d.Year,
    COUNT(DISTINCT s.OrderID) AS OrderCount,
    SUM(s.Quantity) AS UnitsSold,
    ROUND(SUM(s.Quantity * s.UnitPrice), 2) AS GrossSales,
    ROUND(SUM(s.DiscountAmount), 2) AS DiscountAmount,
    ROUND(SUM(s.Quantity * s.UnitPrice - s.DiscountAmount), 2) AS NetRevenue,
    ROUND(SUM(s.Quantity * s.UnitCost), 2) AS TotalCost,
    ROUND(SUM(s.Quantity * s.UnitPrice - s.DiscountAmount) - SUM(s.Quantity * s.UnitCost), 2) AS GrossProfit,
    ROUND(
        (SUM(s.Quantity * s.UnitPrice - s.DiscountAmount) - SUM(s.Quantity * s.UnitCost)) * 100.0 / 
        NULLIF(SUM(s.Quantity * s.UnitPrice - s.DiscountAmount), 0), 2
    ) AS GrossMarginPct,
    ROUND(
        SUM(s.Quantity * s.UnitPrice - s.DiscountAmount) / NULLIF(COUNT(DISTINCT s.OrderID), 0), 2
    ) AS AOV
FROM FactSales s
JOIN DimDate d ON s.DateKey = d.DateKey
GROUP BY d.Year
ORDER BY d.Year;

-- ----------------------------------------------------------------------------
-- Section 3: Regional Performance Breakdown
-- ----------------------------------------------------------------------------
SELECT 
    t.Region,
    t.TerritoryName,
    COUNT(DISTINCT s.OrderID) AS OrderCount,
    ROUND(SUM(s.Quantity * s.UnitPrice - s.DiscountAmount), 2) AS NetRevenue,
    ROUND(SUM(s.Quantity * s.UnitPrice - s.DiscountAmount) - SUM(s.Quantity * s.UnitCost), 2) AS GrossProfit,
    ROUND(
        (SUM(s.Quantity * s.UnitPrice - s.DiscountAmount) - SUM(s.Quantity * s.UnitCost)) * 100.0 / 
        NULLIF(SUM(s.Quantity * s.UnitPrice - s.DiscountAmount), 0), 2
    ) AS GrossMarginPct
FROM FactSales s
JOIN DimTerritory t ON s.TerritoryKey = t.TerritoryKey
GROUP BY t.Region, t.TerritoryName
ORDER BY t.Region, NetRevenue DESC;

-- ----------------------------------------------------------------------------
-- Section 4: Product Category Breakdown
-- ----------------------------------------------------------------------------
SELECT 
    p.Category,
    COUNT(DISTINCT s.OrderID) AS OrderCount,
    SUM(s.Quantity) AS UnitsSold,
    ROUND(SUM(s.Quantity * s.UnitPrice - s.DiscountAmount), 2) AS NetRevenue,
    ROUND(SUM(s.Quantity * s.UnitPrice - s.DiscountAmount) - SUM(s.Quantity * s.UnitCost), 2) AS GrossProfit,
    ROUND(
        (SUM(s.Quantity * s.UnitPrice - s.DiscountAmount) - SUM(s.Quantity * s.UnitCost)) * 100.0 / 
        NULLIF(SUM(s.Quantity * s.UnitPrice - s.DiscountAmount), 0), 2
    ) AS GrossMarginPct,
    ROUND(SUM(s.DiscountAmount) * 100.0 / NULLIF(SUM(s.Quantity * s.UnitPrice), 0), 2) AS DiscountRatePct
FROM FactSales s
JOIN DimProduct p ON s.ProductKey = p.ProductKey
GROUP BY p.Category
ORDER BY NetRevenue DESC;

-- ----------------------------------------------------------------------------
-- Section 5: Actual vs Quota Target Reconciliation (by YearMonth)
-- ----------------------------------------------------------------------------
WITH Actuals AS (
    SELECT 
        d.YearMonth,
        s.TerritoryKey,
        s.SalespersonKey,
        SUM(s.Quantity * s.UnitPrice - s.DiscountAmount) AS ActualRevenue,
        SUM(s.Quantity * s.UnitPrice - s.DiscountAmount) - SUM(s.Quantity * s.UnitCost) AS ActualProfit
    FROM FactSales s
    JOIN DimDate d ON s.DateKey = d.DateKey
    GROUP BY d.YearMonth, s.TerritoryKey, s.SalespersonKey
),
TargetSummary AS (
    SELECT 
        YearMonth,
        TerritoryKey,
        SalespersonKey,
        SUM(RevenueTarget) AS TargetRevenue,
        SUM(ProfitTarget) AS TargetProfit
    FROM FactTargets
    GROUP BY YearMonth, TerritoryKey, SalespersonKey
)
SELECT 
    t.YearMonth,
    ROUND(SUM(a.ActualRevenue), 2) AS TotalActualRevenue,
    ROUND(SUM(t.TargetRevenue), 2) AS TotalTargetRevenue,
    ROUND(SUM(a.ActualRevenue) - SUM(t.TargetRevenue), 2) AS RevenueVariance,
    ROUND(SUM(a.ActualRevenue) * 100.0 / NULLIF(SUM(t.TargetRevenue), 0), 2) AS TargetAttainmentPct,
    ROUND(SUM(a.ActualProfit), 2) AS TotalActualProfit,
    ROUND(SUM(t.TargetProfit), 2) AS TotalTargetProfit,
    ROUND(SUM(a.ActualProfit) * 100.0 / NULLIF(SUM(t.TargetProfit), 0), 2) AS ProfitAttainmentPct
FROM TargetSummary t
LEFT JOIN Actuals a 
    ON t.YearMonth = a.YearMonth 
   AND t.TerritoryKey = a.TerritoryKey 
   AND t.SalespersonKey = a.SalespersonKey
GROUP BY t.YearMonth
ORDER BY t.YearMonth;
