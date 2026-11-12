-- ============================================================================
-- Enterprise Sales & Revenue Intelligence System
-- 02_data_profiling.sql: Data Quality & Profiling Suite
-- SRS Reference: Section 4 (FR-02) and Section 5.4 (Data Quality Rules)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Check 1: Primary Key Uniqueness & Nullability on FactSales
-- Requirement: OrderLineID must be unique and non-null
-- ----------------------------------------------------------------------------
SELECT 
    'FactSales PK Check' AS CheckName,
    COUNT(*) AS TotalRows,
    COUNT(OrderLineID) AS NonNullKeys,
    COUNT(DISTINCT OrderLineID) AS UniqueKeys,
    COUNT(*) - COUNT(DISTINCT OrderLineID) AS DuplicateKeyCount,
    CASE WHEN COUNT(*) = COUNT(DISTINCT OrderLineID) AND COUNT(*) = COUNT(OrderLineID) 
         THEN 'PASS' ELSE 'FAIL' END AS Status
FROM FactSales;

-- Detailed identification of duplicates if any:
SELECT 
    OrderLineID, 
    COUNT(*) AS Occurrences
FROM FactSales
GROUP BY OrderLineID
HAVING COUNT(*) > 1;

-- ----------------------------------------------------------------------------
-- Check 2: Referential Integrity (Orphan Foreign Keys)
-- Requirement: Every foreign key in FactSales must exist in the respective dimension
-- ----------------------------------------------------------------------------
SELECT 
    'Orphan Foreign Keys Check' AS CheckName,
    (SELECT COUNT(*) FROM FactSales s LEFT JOIN DimDate d ON s.DateKey = d.DateKey WHERE d.DateKey IS NULL) AS MissingDateKeys,
    (SELECT COUNT(*) FROM FactSales s LEFT JOIN DimCustomer c ON s.CustomerKey = c.CustomerKey WHERE c.CustomerKey IS NULL) AS MissingCustomerKeys,
    (SELECT COUNT(*) FROM FactSales s LEFT JOIN DimProduct p ON s.ProductKey = p.ProductKey WHERE p.ProductKey IS NULL) AS MissingProductKeys,
    (SELECT COUNT(*) FROM FactSales s LEFT JOIN DimSalesperson sp ON s.SalespersonKey = sp.SalespersonKey WHERE sp.SalespersonKey IS NULL) AS MissingSalespersonKeys,
    (SELECT COUNT(*) FROM FactSales s LEFT JOIN DimTerritory t ON s.TerritoryKey = t.TerritoryKey WHERE t.TerritoryKey IS NULL) AS MissingTerritoryKeys;

-- ----------------------------------------------------------------------------
-- Check 3: Implausible and Negative Values
-- Requirement: Quantity, unit price, cost, discounts must follow business policy
-- ----------------------------------------------------------------------------
SELECT 
    'Value Plausibility Check' AS CheckName,
    SUM(CASE WHEN Quantity < 0 THEN 1 ELSE 0 END) AS NegativeQuantityCount,
    SUM(CASE WHEN Quantity = 0 THEN 1 ELSE 0 END) AS ZeroQuantityCount,
    SUM(CASE WHEN UnitPrice <= 0 THEN 1 ELSE 0 END) AS InvalidUnitPriceCount,
    SUM(CASE WHEN UnitCost <= 0 THEN 1 ELSE 0 END) AS InvalidUnitCostCount,
    SUM(CASE WHEN DiscountAmount < 0 THEN 1 ELSE 0 END) AS NegativeDiscountCount,
    SUM(CASE WHEN DiscountAmount > (Quantity * UnitPrice) THEN 1 ELSE 0 END) AS DiscountExceedsGrossCount
FROM FactSales;

-- ----------------------------------------------------------------------------
-- Check 4: Date Range Coverage & Null Dates
-- Requirement: Coverage must span between 2024-01-01 and current operational date
-- ----------------------------------------------------------------------------
SELECT 
    'Date Boundary Check' AS CheckName,
    MIN(OrderDate) AS EarliestSaleDate,
    MAX(OrderDate) AS LatestSaleDate,
    SUM(CASE WHEN OrderDate IS NULL THEN 1 ELSE 0 END) AS NullOrderDates,
    SUM(CASE WHEN DateKey IS NULL THEN 1 ELSE 0 END) AS NullDateKeys
FROM FactSales;

-- ----------------------------------------------------------------------------
-- Check 5: Target Grain Integrity
-- Requirement: Target data must have exactly one record per YearMonth, Salesperson, and Territory
-- ----------------------------------------------------------------------------
SELECT 
    'Target Grain Uniqueness Check' AS CheckName,
    COUNT(*) AS TotalTargetRows,
    COUNT(DISTINCT YearMonth || '-' || CAST(SalespersonKey AS VARCHAR) || '-' || CAST(TerritoryKey AS VARCHAR)) AS DistinctTargetGrains,
    CASE 
        WHEN COUNT(*) = COUNT(DISTINCT YearMonth || '-' || CAST(SalespersonKey AS VARCHAR) || '-' || CAST(TerritoryKey AS VARCHAR))
        THEN 'PASS' ELSE 'FAIL' 
    END AS Status
FROM FactTargets;

-- ----------------------------------------------------------------------------
-- Check 6: Dimension Table Cardinality & Completeness
-- ----------------------------------------------------------------------------
SELECT 'DimCustomer' AS Dimension, COUNT(*) AS RowCount, COUNT(DISTINCT CustomerID) AS DistinctNaturalKeys, SUM(CASE WHEN CustomerName IS NULL THEN 1 ELSE 0 END) AS NullNames FROM DimCustomer
UNION ALL
SELECT 'DimProduct', COUNT(*), COUNT(DISTINCT ProductID), SUM(CASE WHEN ProductName IS NULL THEN 1 ELSE 0 END) FROM DimProduct
UNION ALL
SELECT 'DimSalesperson', COUNT(*), COUNT(DISTINCT SalespersonID), SUM(CASE WHEN SalespersonName IS NULL THEN 1 ELSE 0 END) FROM DimSalesperson
UNION ALL
SELECT 'DimTerritory', COUNT(*), COUNT(DISTINCT TerritoryName), SUM(CASE WHEN TerritoryName IS NULL THEN 1 ELSE 0 END) FROM DimTerritory
UNION ALL
SELECT 'DimDate', COUNT(*), COUNT(DISTINCT Date), SUM(CASE WHEN Date IS NULL THEN 1 ELSE 0 END) FROM DimDate;
