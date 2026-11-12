# System Architecture & Semantic Data Model

## 1. Architectural Overview
The **Enterprise Sales & Revenue Intelligence System** is engineered according to Kimball dimensional modeling principles, implementing a pure Star Schema with conformed dimensions to support fast, flexible analytical reporting across Power BI Desktop and Power BI Service.

```mermaid
erDiagram
    DimDate ||--o{ FactSales : "filters (DateKey)"
    DimCustomer ||--o{ FactSales : "filters (CustomerKey)"
    DimProduct ||--o{ FactSales : "filters (ProductKey)"
    DimSalesperson ||--o{ FactSales : "filters (SalespersonKey)"
    DimTerritory ||--o{ FactSales : "filters (TerritoryKey)"

    DimDate ||--o{ FactTargets : "filters (DateKey)"
    DimTerritory ||--o{ FactTargets : "filters (TerritoryKey)"
    DimSalesperson ||--o{ FactTargets : "filters (SalespersonKey)"

    UserSecurityMapping ||--o{ DimTerritory : "secures (TerritoryKey)"

    FactSales {
        bigint OrderLineID PK
        string OrderID
        date OrderDate
        int DateKey FK
        int CustomerKey FK
        int ProductKey FK
        int SalespersonKey FK
        int TerritoryKey FK
        int Quantity
        decimal UnitPrice
        decimal DiscountAmount
        decimal UnitCost
    }

    FactTargets {
        int TargetKey PK
        date TargetDate
        int DateKey FK
        string YearMonth
        int TerritoryKey FK
        int SalespersonKey FK
        decimal RevenueTarget
        decimal ProfitTarget
    }

    DimDate {
        int DateKey PK
        date Date
        int Year
        string Quarter
        string YearQuarter
        int Month
        string MonthName
        string YearMonth
        int Week
        int DayOfWeek
        int IsWorkingDay
    }

    DimCustomer {
        int CustomerKey PK
        string CustomerID
        string CustomerName
        string Segment
        string City
        string State
        string Country
        string Region
        date AcquisitionDate
    }

    DimProduct {
        int ProductKey PK
        string ProductID
        string ProductName
        string Category
        string Subcategory
        string Brand
        decimal StandardCost
        decimal ListPrice
    }

    DimSalesperson {
        int SalespersonKey PK
        string SalespersonID
        string SalespersonName
        string Email
        string Manager
        int TerritoryKey FK
    }

    DimTerritory {
        int TerritoryKey PK
        string TerritoryName
        string Region
        string Country
    }

    UserSecurityMapping {
        string UserEmail PK
        int TerritoryKey FK
        string Role
    }
```

---

## 2. Granularity & Multi-Fact Modeling

### FactSales Grain
* **Grain:** One record per individual order line item.
* **Primary Key:** `OrderLineID` (Surrogate integer).
* **Distinct Order Count:** Handled via explicit `DISTINCTCOUNT(FactSales[OrderID])` to avoid treating lines as orders.

### FactTargets Grain
* **Grain:** One record per calendar month, per salesperson, per assigned territory.
* **Target Period:** First calendar day of each month (`YYYY-MM-01`), linking to `DimDate[DateKey]`.
* **Grain Alignment:** Targets are NOT directly joined to transaction lines, which would cause Cartesian fan-out and double counting. Instead, both fact tables connect to shared conformed dimensions (`DimDate`, `DimSalesperson`, `DimTerritory`). DAX measures calculate variances cleanly at whatever level of aggregation is selected.

---

## 3. Relationship Specifications
| From Table | From Column | To Table | To Column | Cardinality | Filter Direction |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `FactSales` | `DateKey` | `DimDate` | `DateKey` | Many-to-One | Single (DimDate -> FactSales) |
| `FactSales` | `CustomerKey` | `DimCustomer` | `CustomerKey` | Many-to-One | Single (DimCustomer -> FactSales) |
| `FactSales` | `ProductKey` | `DimProduct` | `ProductKey` | Many-to-One | Single (DimProduct -> FactSales) |
| `FactSales` | `SalespersonKey` | `DimSalesperson` | `SalespersonKey` | Many-to-One | Single (DimSalesperson -> FactSales) |
| `FactSales` | `TerritoryKey` | `DimTerritory` | `TerritoryKey` | Many-to-One | Single (DimTerritory -> FactSales) |
| `FactTargets` | `DateKey` | `DimDate` | `DateKey` | Many-to-One | Single (DimDate -> FactTargets) |
| `FactTargets` | `TerritoryKey` | `DimTerritory` | `TerritoryKey` | Many-to-One | Single (DimTerritory -> FactTargets) |
| `FactTargets` | `SalespersonKey` | `DimSalesperson` | `SalespersonKey` | Many-to-One | Single (DimSalesperson -> FactTargets) |
| `UserSecurityMapping` | `TerritoryKey` | `DimTerritory` | `TerritoryKey` | Many-to-One | Bi-directional (RLS filter propagation) |

---

## 4. End-to-End Data Pipeline Flow

```mermaid
flowchart LR
    A[Staging CSV / SQL OLTP] -->|Extract & Validate| B[Power Query / Python ETL]
    B -->|Cleanse, Quarantine, Cast| C[Curated Star Schema Tables]
    C -->|Import / Refresh| D[Power BI Semantic Model]
    D -->|Evaluate DAX Measures| E[Interactive Report Visuals RP01-RP06]
    D -->|Apply Dynamic Security| F[Governed User Experience]
```

1. **Extraction:** Raw CSVs or relational SQL tables ingested.
2. **Data Profiling & Cleansing:** Anomalies (negative quantities, duplicate line keys, orphan customer keys) identified and quarantined.
3. **Surrogate Key Generation & Conformation:** Dimensions generated with business keys and integer surrogate keys. Unknown dimension members (Key = 0) inserted for resilience.
4. **Semantic Model:** Import mode with VertiPaq column store compression.
5. **Consumption:** 6 distinct report pages consumed via Web Browser or Power BI Mobile.
