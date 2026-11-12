# Enterprise Data Dictionary

## 1. FactSales (Primary Transaction Fact Table)
* **Grain:** One row per physical order line item.
* **Storage Mode:** Import (VertiPaq Compressed).

| Field Name | Data Type | Nullable | Key Type | Description & Business Rules |
| :--- | :--- | :--- | :--- | :--- |
| `OrderLineID` | BigInt / Integer | NO | Primary Key | Unique line identifier. Must be non-null and unique across all transactions. |
| `OrderID` | Text | NO | Degenerate Key | Natural transaction order reference. Repeats across multiple line items. |
| `OrderDate` | Date | NO | Attribute | Commercial transaction recognition date. |
| `DateKey` | Integer | NO | Foreign Key | Integer representation of date (`YYYYMMDD`). Joins to `DimDate[DateKey]`. |
| `CustomerKey` | Integer | NO | Foreign Key | Surrogate key referencing `DimCustomer[CustomerKey]`. Default `0` for unassigned. |
| `ProductKey` | Integer | NO | Foreign Key | Surrogate key referencing `DimProduct[ProductKey]`. |
| `SalespersonKey` | Integer | NO | Foreign Key | Surrogate key referencing `DimSalesperson[SalespersonKey]`. |
| `TerritoryKey` | Integer | NO | Foreign Key | Surrogate key referencing `DimTerritory[TerritoryKey]`. |
| `Quantity` | Integer | NO | Measure Baseline | Number of units delivered. Must be strictly positive (> 0) in production fact. |
| `UnitPrice` | Decimal(12,2) | NO | Measure Baseline | Unit selling price billed before line discount. Non-negative. |
| `DiscountAmount`| Decimal(12,2) | NO | Measure Baseline | Total discount granted for this line. Cannot exceed `Quantity * UnitPrice`. |
| `UnitCost` | Decimal(12,2) | NO | Measure Baseline | Standard unit manufacturing or procurement cost. |

---

## 2. FactTargets (Quota & Quota Period Fact Table)
* **Grain:** One row per calendar month, per salesperson, per territory.

| Field Name | Data Type | Nullable | Key Type | Description & Business Rules |
| :--- | :--- | :--- | :--- | :--- |
| `TargetKey` | Integer | NO | Primary Key | Surrogate target sequence key. |
| `TargetDate` | Date | NO | Attribute | First calendar day of the target month (`YYYY-MM-01`). |
| `DateKey` | Integer | NO | Foreign Key | Joins to `DimDate[DateKey]`. |
| `YearMonth` | Text | NO | Attribute | Formatted reporting period (e.g., `2025-04`). |
| `TerritoryKey` | Integer | NO | Foreign Key | Assigned territory. Joins to `DimTerritory[TerritoryKey]`. |
| `SalespersonKey`| Integer | NO | Foreign Key | Quota recipient. Joins to `DimSalesperson[SalespersonKey]`. |
| `RevenueTarget`| Decimal(14,2) | NO | Measure Baseline | Allocated commercial net revenue target. |
| `ProfitTarget` | Decimal(14,2) | NO | Measure Baseline | Allocated gross profit target. |

---

## 3. DimDate (Conformed Time Dimension)
* **Grain:** One row per calendar day. Marked as Date Table in semantic model.

| Field Name | Data Type | Description & Example Values |
| :--- | :--- | :--- |
| `DateKey` | Integer | Primary key surrogate in `YYYYMMDD` format (e.g. `20250615`). |
| `Date` | Date | Full calendar date (`2025-06-15`). |
| `Year` | Integer | Calendar year (`2024`, `2025`, `2026`). |
| `Quarter` | Text | Quarter indicator (`Q1`, `Q2`, `Q3`, `Q4`). |
| `YearQuarter` | Text | Formatted year and quarter (`2025-Q2`). |
| `Month` | Integer | Month index (`1` through `12`). |
| `MonthName` | Text | Full month title (`January` through `December`). Sorted by `Month`. |
| `MonthShort` | Text | Three-letter abbreviation (`Jan` through `Dec`). Sorted by `Month`. |
| `YearMonth` | Text | Standard analytical sorting string (`2025-06`). |
| `Week` | Integer | Calendar week of year (1 - 53). |
| `DayOfWeek` | Integer | Day index (1 = Monday, 7 = Sunday). |
| `DayName` | Text | Name of day (`Monday`, `Tuesday`, etc.). |
| `IsWorkingDay` | Integer | Binary flag: `1` for Monday-Friday, `0` for Saturday-Sunday. |

---

## 4. DimCustomer (Customer Master Dimension)
* **Grain:** One row per registered customer account.

| Field Name | Data Type | Description |
| :--- | :--- | :--- |
| `CustomerKey` | Integer | Primary surrogate key. Key `0` reserved for Unknown/Unassigned. |
| `CustomerID` | Text | Natural customer identifier (e.g., `CUST-0012`). |
| `CustomerName` | Text | Registered company or individual commercial account name. |
| `Segment` | Text | Commercial segmentation (`Corporate`, `Enterprise B2B`, `Consumer`, `Home Office`). |
| `City` | Text | Registered operating city. |
| `State` | Text | State or province abbreviation/name. |
| `Country` | Text | Operating country (e.g., `United States`, `Germany`). |
| `Region` | Text | Macro-region (`Americas`, `EMEA`, `APAC`). |
| `AcquisitionDate`| Date | Initial account activation or onboarding date. |

---

## 5. DimProduct (Product Catalog Dimension)
* **Grain:** One row per commercial SKU.

| Field Name | Data Type | Description |
| :--- | :--- | :--- |
| `ProductKey` | Integer | Primary surrogate key. Key `0` reserved for Unknown. |
| `ProductID` | Text | Natural product SKU (e.g., `PROD-004`). |
| `ProductName` | Text | Commercial product name. |
| `Category` | Text | Primary merchandise category (`Technology`, `Office Solutions`, etc.). |
| `Subcategory` | Text | Specific sub-classification (`Laptops & Workstations`, `Networking`, etc.). |
| `Brand` | Text | Product manufacturer or internal brand. |
| `StandardCost`| Decimal(12,2) | Baseline standard production or wholesale cost. |
| `ListPrice` | Decimal(12,2) | Standard manufacturer's suggested retail price (MSRP). |

---

## 6. DimSalesperson & DimTerritory
* **DimSalesperson:** `SalespersonKey`, `SalespersonID`, `SalespersonName`, `Email`, `Manager`, `TerritoryKey`.
* **DimTerritory:** `TerritoryKey`, `TerritoryName`, `Region`, `Country`.
* **UserSecurityMapping:** `MappingID`, `UserEmail`, `TerritoryKey`, `Role`.
