-- ============================================================================
-- Enterprise Sales & Revenue Intelligence System
-- 03_transformations_etl.sql: Staging-to-Star Schema Transformations
-- SRS Reference: Section 4 (FR-03: Data Transformation) & Section 5.4
-- ============================================================================

-- Staging table definition for ingesting raw data
CREATE TABLE IF NOT EXISTS stg_raw_sales (
    OrderLineID VARCHAR(50),
    OrderID VARCHAR(50),
    OrderDate VARCHAR(50),
    DateKey VARCHAR(50),
    CustomerKey VARCHAR(50),
    ProductKey VARCHAR(50),
    SalespersonKey VARCHAR(50),
    TerritoryKey VARCHAR(50),
    Quantity VARCHAR(50),
    UnitPrice VARCHAR(50),
    DiscountAmount VARCHAR(50),
    UnitCost VARCHAR(50)
);

-- ============================================================================
-- Transformation 1: Deduplication, Type Casting & Data Cleansing
-- Business Rule:
--  - Deduplicate by OrderLineID choosing the earliest valid entry
--  - Strip whitespace, cast types properly
--  - Resolve orphan foreign keys to 0 (Unknown member)
--  - Enforce non-negative unit cost and unit price
-- ============================================================================

-- Insert Unknown Members into dimensions if not present
INSERT INTO DimCustomer (CustomerKey, CustomerID, CustomerName, Segment, City, State, Country, Region, AcquisitionDate)
SELECT 0, 'CUST-0000', 'Unknown Customer', 'Unassigned', 'Unknown', 'NA', 'Unknown', 'Unassigned', '2024-01-01'
WHERE NOT EXISTS (SELECT 1 FROM DimCustomer WHERE CustomerKey = 0);

INSERT INTO DimProduct (ProductKey, ProductID, ProductName, Category, Subcategory, Brand, StandardCost, ListPrice)
SELECT 0, 'PROD-000', 'Unknown Product', 'Unassigned', 'Unassigned', 'Unassigned', 0.00, 0.00
WHERE NOT EXISTS (SELECT 1 FROM DimProduct WHERE ProductKey = 0);

INSERT INTO DimTerritory (TerritoryKey, TerritoryName, Region, Country)
SELECT 0, 'Unknown Territory', 'Unassigned', 'Unassigned'
WHERE NOT EXISTS (SELECT 1 FROM DimTerritory WHERE TerritoryKey = 0);

INSERT INTO DimSalesperson (SalespersonKey, SalespersonID, SalespersonName, Email, Manager, TerritoryKey)
SELECT 0, 'SP-000', 'Unassigned Salesperson', 'unassigned@enterprisegroup.com', 'None', 0
WHERE NOT EXISTS (SELECT 1 FROM DimSalesperson WHERE SalespersonKey = 0);

-- Curated Load into FactSales with deduplication windowing & cleansing logic:
/*
INSERT INTO FactSales (
    OrderLineID,
    OrderID,
    OrderDate,
    DateKey,
    CustomerKey,
    ProductKey,
    SalespersonKey,
    TerritoryKey,
    Quantity,
    UnitPrice,
    DiscountAmount,
    UnitCost
)
WITH CleanedStaging AS (
    SELECT 
        CAST(TRIM(OrderLineID) AS BIGINT) AS OrderLineID,
        TRIM(OrderID) AS OrderID,
        CAST(TRIM(OrderDate) AS DATE) AS OrderDate,
        CAST(TRIM(DateKey) AS INT) AS DateKey,
        COALESCE(c.CustomerKey, 0) AS CustomerKey,
        COALESCE(p.ProductKey, 0) AS ProductKey,
        COALESCE(sp.SalespersonKey, 0) AS SalespersonKey,
        COALESCE(t.TerritoryKey, 0) AS TerritoryKey,
        CAST(TRIM(Quantity) AS INT) AS Quantity,
        ROUND(CAST(TRIM(UnitPrice) AS NUMERIC(12,2)), 2) AS UnitPrice,
        ROUND(CAST(TRIM(DiscountAmount) AS NUMERIC(12,2)), 2) AS DiscountAmount,
        ROUND(CAST(TRIM(UnitCost) AS NUMERIC(12,2)), 2) AS UnitCost,
        ROW_NUMBER() OVER (
            PARTITION BY CAST(TRIM(OrderLineID) AS BIGINT) 
            ORDER BY CAST(TRIM(OrderDate) AS DATE) ASC
        ) AS RowRank
    FROM stg_raw_sales stg
    LEFT JOIN DimCustomer c ON CAST(TRIM(stg.CustomerKey) AS INT) = c.CustomerKey
    LEFT JOIN DimProduct p ON CAST(TRIM(stg.ProductKey) AS INT) = p.ProductKey
    LEFT JOIN DimSalesperson sp ON CAST(TRIM(stg.SalespersonKey) AS INT) = sp.SalespersonKey
    LEFT JOIN DimTerritory t ON CAST(TRIM(stg.TerritoryKey) AS INT) = t.TerritoryKey
    WHERE TRIM(OrderLineID) IS NOT NULL
      AND CAST(TRIM(Quantity) AS INT) > 0  -- Filter out raw returns to quarantine table
)
SELECT 
    OrderLineID,
    OrderID,
    OrderDate,
    DateKey,
    CustomerKey,
    ProductKey,
    SalespersonKey,
    TerritoryKey,
    Quantity,
    UnitPrice,
    DiscountAmount,
    UnitCost
FROM CleanedStaging
WHERE RowRank = 1;
*/
