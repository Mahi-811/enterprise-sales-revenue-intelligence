-- ============================================================================
-- Enterprise Sales & Revenue Intelligence System
-- 01_schema_ddl.sql: Relational Star Schema DDL
-- Platform: Compatible with PostgreSQL, SQL Server (T-SQL), MySQL 8.0+, SQLite
-- SRS Reference: Section 5 (Data Requirements and Logical Model)
-- ============================================================================

-- Drop tables if existing (in reverse dependency order)
DROP TABLE IF EXISTS FactSales;
DROP TABLE IF EXISTS FactTargets;
DROP TABLE IF EXISTS UserSecurityMapping;
DROP TABLE IF EXISTS DimSalesperson;
DROP TABLE IF EXISTS DimProduct;
DROP TABLE IF EXISTS DimCustomer;
DROP TABLE IF EXISTS DimTerritory;
DROP TABLE IF EXISTS DimDate;
DROP TABLE IF EXISTS stg_sales_transactions;

-- ============================================================================
-- 1. DIMENSION TABLES
-- ============================================================================

-- DimDate: Dedicated calendar dimension for time intelligence
CREATE TABLE DimDate (
    DateKey INT PRIMARY KEY,                     -- YYYYMMDD integer surrogate key
    Date DATE NOT NULL UNIQUE,                   -- Calendar date
    Year INT NOT NULL,                           -- Calendar year (e.g. 2024, 2025, 2026)
    Quarter VARCHAR(2) NOT NULL,                 -- Quarter indicator (Q1, Q2, Q3, Q4)
    YearQuarter VARCHAR(7) NOT NULL,             -- Combined Year-Quarter (e.g. 2024-Q1)
    Month INT NOT NULL,                          -- Month number (1 - 12)
    MonthName VARCHAR(20) NOT NULL,              -- Full month name (e.g. January)
    MonthShort VARCHAR(3) NOT NULL,              -- Abbreviated month name (e.g. Jan)
    YearMonth VARCHAR(7) NOT NULL,               -- Combined Year-Month (e.g. 2024-01)
    Week INT NOT NULL,                           -- Week number of year (1 - 53)
    DayOfWeek INT NOT NULL,                      -- ISO day of week (1 = Monday, 7 = Sunday)
    DayName VARCHAR(15) NOT NULL,                -- Full day name (e.g. Monday)
    IsWorkingDay INT NOT NULL DEFAULT 1          -- 1 = Business day, 0 = Weekend/Holiday
);

-- DimTerritory: Sales geographic hierarchy
CREATE TABLE DimTerritory (
    TerritoryKey INT PRIMARY KEY,                -- Surrogate integer key
    TerritoryName VARCHAR(100) NOT NULL,         -- Territory descriptor
    Region VARCHAR(50) NOT NULL,                 -- Global reporting region (Americas, EMEA, APAC)
    Country VARCHAR(50) NOT NULL                 -- Primary nation
);

-- DimCustomer: Customer master & commercial segmentation
CREATE TABLE DimCustomer (
    CustomerKey INT PRIMARY KEY,                 -- Surrogate integer key
    CustomerID VARCHAR(20) NOT NULL UNIQUE,      -- Natural/Business key
    CustomerName VARCHAR(150) NOT NULL,          -- Account or contact name
    Segment VARCHAR(50) NOT NULL,                -- Corporate, Enterprise B2B, Consumer, Home Office
    City VARCHAR(100) NOT NULL,                  -- Registered city
    State VARCHAR(50) NOT NULL,                  -- State or province
    Country VARCHAR(50) NOT NULL,                -- Country
    Region VARCHAR(50) NOT NULL,                 -- Region
    AcquisitionDate DATE NOT NULL                -- Initial account creation date
);

-- DimProduct: Product hierarchy & costing baseline
CREATE TABLE DimProduct (
    ProductKey INT PRIMARY KEY,                  -- Surrogate integer key
    ProductID VARCHAR(20) NOT NULL UNIQUE,       -- Natural SKU code
    ProductName VARCHAR(150) NOT NULL,           -- Commercial product title
    Category VARCHAR(50) NOT NULL,               -- Product category hierarchy (e.g. Technology)
    Subcategory VARCHAR(50) NOT NULL,            -- Detailed sub-classification
    Brand VARCHAR(50) NOT NULL,                  -- Manufacturer or in-house brand
    StandardCost NUMERIC(12, 2) NOT NULL,        -- Baseline unit production/acquisition cost
    ListPrice NUMERIC(12, 2) NOT NULL            -- Standard catalog price
);

-- DimSalesperson: Sales organization and regional assignment
CREATE TABLE DimSalesperson (
    SalespersonKey INT PRIMARY KEY,              -- Surrogate integer key
    SalespersonID VARCHAR(20) NOT NULL UNIQUE,   -- Employee ID
    SalespersonName VARCHAR(100) NOT NULL,       -- Employee full name
    Email VARCHAR(120) NOT NULL,                 -- Corporate email (used for RLS matching)
    Manager VARCHAR(100) NOT NULL,               -- Direct reporting manager
    TerritoryKey INT NOT NULL,                   -- Assigned primary territory
    CONSTRAINT fk_salesperson_territory FOREIGN KEY (TerritoryKey) REFERENCES DimTerritory(TerritoryKey)
);

-- ============================================================================
-- 2. FACT TABLES
-- ============================================================================

-- FactSales: Order line transaction grain
CREATE TABLE FactSales (
    OrderLineID BIGINT PRIMARY KEY,              -- Unique line identifier
    OrderID VARCHAR(30) NOT NULL,                -- Order header reference (can repeat)
    OrderDate DATE NOT NULL,                     -- Recognition date
    DateKey INT NOT NULL,                        -- FK to DimDate
    CustomerKey INT NOT NULL,                    -- FK to DimCustomer
    ProductKey INT NOT NULL,                     -- FK to DimProduct
    SalespersonKey INT NOT NULL,                 -- FK to DimSalesperson
    TerritoryKey INT NOT NULL,                   -- FK to DimTerritory
    Quantity INT NOT NULL,                       -- Units billed / returned
    UnitPrice NUMERIC(12, 2) NOT NULL,           -- Transaction line unit selling price
    DiscountAmount NUMERIC(12, 2) NOT NULL,      -- Absolute line discount amount
    UnitCost NUMERIC(12, 2) NOT NULL,            -- Transaction unit standard cost
    CONSTRAINT fk_sales_date FOREIGN KEY (DateKey) REFERENCES DimDate(DateKey),
    CONSTRAINT fk_sales_customer FOREIGN KEY (CustomerKey) REFERENCES DimCustomer(CustomerKey),
    CONSTRAINT fk_sales_product FOREIGN KEY (ProductKey) REFERENCES DimProduct(ProductKey),
    CONSTRAINT fk_sales_salesperson FOREIGN KEY (SalespersonKey) REFERENCES DimSalesperson(SalespersonKey),
    CONSTRAINT fk_sales_territory FOREIGN KEY (TerritoryKey) REFERENCES DimTerritory(TerritoryKey)
);

-- FactTargets: Monthly quota grain by salesperson & territory
CREATE TABLE FactTargets (
    TargetKey INT PRIMARY KEY,                   -- Surrogate target record key
    TargetDate DATE NOT NULL,                    -- Period anchor (YYYY-MM-01)
    DateKey INT NOT NULL,                        -- FK to DimDate (month start)
    YearMonth VARCHAR(7) NOT NULL,               -- Reporting period YYYY-MM
    TerritoryKey INT NOT NULL,                   -- Assigned territory
    SalespersonKey INT NOT NULL,                 -- Quota holder
    RevenueTarget NUMERIC(14, 2) NOT NULL,       -- Commercial revenue quota
    ProfitTarget NUMERIC(14, 2) NOT NULL,        -- Gross profit quota
    CONSTRAINT fk_target_date FOREIGN KEY (DateKey) REFERENCES DimDate(DateKey),
    CONSTRAINT fk_target_territory FOREIGN KEY (TerritoryKey) REFERENCES DimTerritory(TerritoryKey),
    CONSTRAINT fk_target_salesperson FOREIGN KEY (SalespersonKey) REFERENCES DimSalesperson(SalespersonKey),
    CONSTRAINT uq_target_grain UNIQUE (YearMonth, SalespersonKey, TerritoryKey)
);

-- UserSecurityMapping: Table supporting dynamic Row-Level Security (RLS)
CREATE TABLE UserSecurityMapping (
    MappingID INT PRIMARY KEY,
    UserEmail VARCHAR(120) NOT NULL,             -- User Principal Name (UPN)
    TerritoryKey INT NOT NULL,                   -- Authorized territory key (0 = unrestricted/all)
    Role VARCHAR(50) NOT NULL                    -- Business permission role
);

-- ============================================================================
-- 3. PERFORMANCE INDEXES
-- ============================================================================
CREATE INDEX idx_sales_date ON FactSales(DateKey);
CREATE INDEX idx_sales_customer ON FactSales(CustomerKey);
CREATE INDEX idx_sales_product ON FactSales(ProductKey);
CREATE INDEX idx_sales_salesperson ON FactSales(SalespersonKey);
CREATE INDEX idx_sales_territory ON FactSales(TerritoryKey);
CREATE INDEX idx_sales_order ON FactSales(OrderID);

CREATE INDEX idx_target_period ON FactTargets(DateKey);
CREATE INDEX idx_target_sp ON FactTargets(SalespersonKey);
CREATE INDEX idx_target_terr ON FactTargets(TerritoryKey);
