# SOFTWARE REQUIREMENTS SPECIFICATION
## Enterprise Sales & Revenue Intelligence System
**Project Type:** Business Intelligence / Power BI Engineering  
**Document Version:** 1.0 | **Status:** Proposed Baseline  
**Prepared:** 12 November 2026  

---

## Document Control
| Field | Value |
| :--- | :--- |
| **Document title** | Software Requirements Specification – Enterprise Sales & Revenue Intelligence System |
| **Version** | 1.0 |
| **Status** | Proposed baseline |
| **Primary platform** | Microsoft Power BI Desktop and Power BI Service |
| **Supporting technologies** | SQL database, Power Query (M), DAX, Excel/CSV, Python |
| **Intended audience** | Project owner, BI developer, data engineer, business stakeholders, portfolio reviewers |
| **Purpose** | Define scope, requirements, data design, report behaviour, security, and acceptance criteria. |

---

## 1. Introduction

### 1.1 Purpose
This SRS defines the requirements for an Enterprise Sales & Revenue Intelligence System built with Microsoft Power BI. The system will consolidate sales-related data, transform it into a governed analytical model, and provide interactive reports for monitoring revenue, profitability, sales performance, customer behaviour, product performance, and targets.

### 1.2 Project Scope
The solution is a portfolio-grade business intelligence application that simulates the reporting needs of a mid-sized retail, distribution, or B2B organisation. It will use a relational analytical model and a set of Power BI report pages. It is not intended to process transactions, replace an ERP/CRM platform, or provide real-time operational control.
* **In scope:** ingestion of structured sales, customer, product, territory, salesperson, target, and calendar data.
* **In scope:** data cleaning, validation, transformation, dimensional modelling, DAX measures, interactive reports, row-level security demonstration, refresh configuration, and performance testing.
* **In scope:** documented business definitions, test cases, source-to-target mappings, and deployment instructions.
* **Out of scope:** order entry, payment processing, inventory transaction execution, CRM workflow automation, predictive ML production deployment, and guaranteed live connectivity to third-party systems.

### 1.3 Intended Users
| User role | Primary needs |
| :--- | :--- |
| **Executive / leadership** | High-level revenue, profit, growth, target attainment, and risk indicators. |
| **Sales manager** | Team, territory, salesperson, pipeline-independent sales results, and target comparisons. |
| **Regional manager** | Regional performance, product mix, customer trends, and territory comparisons. |
| **Finance analyst** | Revenue, discounts, cost, gross profit, margin, and period comparisons. |
| **BI administrator / developer** | Data refresh, model maintenance, security, data quality, and report performance. |

### 1.4 Definitions and Acronyms
| Term | Definition |
| :--- | :--- |
| **BI** | Business Intelligence |
| **DAX** | Data Analysis Expressions, used for semantic model calculations. |
| **ETL / ELT** | Extract, Transform, Load / Extract, Load, Transform. |
| **Fact table** | A table containing measurable business events, such as sales lines. |
| **Dimension table** | A descriptive table used to filter and group facts. |
| **RLS** | Row-Level Security. |
| **YTD / QTD / MTD** | Year-to-date / Quarter-to-date / Month-to-date. |
| **YoY / MoM** | Year-over-year / Month-over-month. |
| **Star schema** | A dimensional model with fact tables related to descriptive dimensions. |

---

## 2. Overall Description

### 2.1 Product Perspective
The system will be implemented as a Power BI semantic model and report suite. Source data may be stored in SQL Server, PostgreSQL, MySQL, or a clearly documented local relational database. CSV or Excel files may be used for initial data loading or where a source system is unavailable. Power Query will perform repeatable transformations; DAX will provide business calculations.

### 2.2 Operating Environment
* Development: Power BI Desktop on Windows.
* Publication: Power BI Service workspace, subject to available licensing and tenant permissions.
* Data source: SQL database and/or controlled CSV/Excel files.
* Git repository with PBIP project files, SQL scripts, documentation, and sample data.
* Report consumption: modern web browser through Power BI Service, or Power BI Desktop for local review.

### 2.3 Design Principles
* Use a star schema and single-direction relationships by default.
* Separate raw/staging transformations from the semantic model where practical.
* Define each KPI once and reuse it across report pages.
* Use explicit measures rather than implicit aggregations for business-critical metrics.
* Make filters, definitions, refresh timestamps, and data limitations visible to report users.
* Optimise for usability, correctness, maintainability, and performance rather than visual decoration alone.

---

## 3. Business Requirements
| ID | Requirement | Priority |
| :--- | :--- | :--- |
| **BR-01** | Provide a consolidated view of sales revenue and profitability across the organisation. | Must |
| **BR-02** | Allow users to compare actual performance with targets across time, territory, product, and salesperson. | Must |
| **BR-03** | Identify revenue and profit trends, underperforming segments, and material variances. | Must |
| **BR-04** | Enable users to move from executive summaries to detailed transaction-level analysis. | Must |
| **BR-05** | Provide consistent, documented KPI definitions across all report pages. | Must |
| **BR-06** | Restrict sensitive regional or team-level data according to the viewer’s authorised scope. | Should |
| **BR-07** | Support scheduled refresh and communicate the last successful refresh time. | Should |

---

## 4. Functional Requirements
| ID | Feature | Requirement | Priority |
| :--- | :--- | :--- | :--- |
| **FR-01** | Data ingestion | The solution shall ingest sales transaction data and the supporting customer, product, salesperson, territory, target, and date data. | Must |
| **FR-02** | Data validation | The solution shall identify missing keys, duplicate transaction-line identifiers, invalid dates, negative or implausible values, and orphaned dimension references. | Must |
| **FR-03** | Data transformation | The solution shall standardise column names and data types, trim text, handle nulls according to documented rules, and derive required business attributes. | Must |
| **FR-04** | Dimensional model | The solution shall implement a documented star schema with a sales fact table and conformed dimensions. | Must |
| **FR-05** | KPI calculations | The solution shall calculate revenue, cost, gross profit, gross margin, order count, units sold, average order value, discounts, and target attainment. | Must |
| **FR-06** | Time intelligence | The solution shall provide MTD, QTD, YTD, prior-period, YoY, and MoM measures where the underlying date coverage permits. | Must |
| **FR-07** | Interactive filtering | Users shall be able to filter by date, region, territory, product category, product, customer segment, and salesperson. | Must |
| **FR-08** | Drill-down | Users shall be able to drill from year to quarter, month, and day, and from product category to product where applicable. | Must |
| **FR-09** | Drill-through | Users shall be able to open detail pages from summary visuals while retaining relevant filter context. | Should |
| **FR-10** | Tooltips | Key visuals shall provide contextual tooltips with metric definitions or supporting measures. | Should |
| **FR-11** | Target comparison | The solution shall compare actual sales and profit against targets at supported reporting grains. | Must |
| **FR-12** | Export | Authorised users shall be able to export permitted summarized or underlying data, subject to tenant settings. | Could |
| **FR-13** | Security | The solution shall support dynamic or static RLS for region/team restrictions. | Should |
| **FR-14** | Refresh | The solution shall support a documented refresh process and expose the latest refresh date/time. | Should |
| **FR-15** | Navigation | The report shall provide consistent navigation, page titles, reset-filter guidance, and clear selected-filter context. | Must |
| **FR-16** | Error/empty states | The report shall show meaningful empty-state messages when filters return no records and avoid misleading zero or blank displays. | Should |

---

## 5. Data Requirements and Model

### 5.1 Proposed Logical Model
* `FactSales` (OrderLineID [PK], OrderID, OrderDate, DateKey [FK], CustomerKey [FK], ProductKey [FK], SalespersonKey [FK], TerritoryKey [FK], Quantity, UnitPrice, DiscountAmount, UnitCost)
* `DimDate` (DateKey [PK], Date, Year, Quarter, YearQuarter, Month, MonthName, MonthShort, YearMonth, Week, DayOfWeek, DayName, IsWorkingDay)
* `DimCustomer` (CustomerKey [PK], CustomerID, CustomerName, Segment, City, State, Country, Region, AcquisitionDate)
* `DimProduct` (ProductKey [PK], ProductID, ProductName, Category, Subcategory, Brand, StandardCost, ListPrice)
* `DimSalesperson` (SalespersonKey [PK], SalespersonID, SalespersonName, Email, Manager, TerritoryKey [FK])
* `DimTerritory` (TerritoryKey [PK], TerritoryName, Region, Country)
* `FactTargets` (TargetKey [PK], TargetDate, DateKey [FK], YearMonth, TerritoryKey [FK], SalespersonKey [FK], RevenueTarget, ProfitTarget)
* `UserSecurityMapping` (MappingID, UserEmail, TerritoryKey, Role)

---

## 6. Report and Dashboard Specifications
* **RP-01 Executive Overview:** KPI cards (Total Revenue, Gross Profit, Margin %, Orders, AOV, Quota Attainment), Revenue Trend, Region Doughnut, Category Column Chart, Top 5 Products.
* **RP-02 Sales Performance:** Quota Attainment Matrix, Salesperson Rankings, Target Variance.
* **RP-03 Product Performance:** Product Category Breakdown, Margin Analysis, 32 SKU Catalog.
* **RP-04 Customer Insights:** Customer Segments, Active Customer Penetration, Average Revenue per Account.
* **RP-05 Revenue & Profitability:** Financial Bridge / Waterfall, Gross to Net Reconciliation, COGS Cost Ratio.
* **RP-06 Transaction Detail:** Filterable, searchable line-level ledger with CSV export capabilities.

---

## 7. Non-Functional Requirements
* **NFR-01 Performance:** Visual queries complete within 5 seconds on test environments.
* **NFR-02 Refresh:** Full refresh executes in under 10 minutes.
* **NFR-03 Scalability:** Star schema optimized with surrogate integer keys and reduced cardinality.
* **NFR-04 Reliability:** Detectable refresh failure state and visible timestamps.
* **NFR-05 Maintainability:** Fully documented measure library and clean TMDL structure.
* **NFR-06 Usability:** Self-serve filtering without developer assistance.
* **NFR-07 Accessibility:** WCAG 2.1 AA compliant color palette and dual cues.
* **NFR-08 Portability:** Fully reproducible through synthetic generators and SQL DDL.
* **NFR-09 Data Integrity:** 100% reconciliation against ground-truth SQL scripts.
* **NFR-10 Privacy:** Anonymized synthetic data suitable for open publication.

---

## 8. Appendix A: KPI Definitions
* **Gross Sales:** $\sum(\text{Quantity} \times \text{UnitPrice})$
* **Discount Amount:** $\sum\text{DiscountAmount}$
* **Net Sales / Revenue:** $\text{Gross Sales} - \text{Discount Amount}$
* **Cost of Goods Sold (COGS):** $\sum(\text{Quantity} \times \text{UnitCost})$
* **Gross Profit:** $\text{Net Revenue} - \text{COGS}$
* **Gross Margin %:** $\frac{\text{Gross Profit}}{\text{Net Revenue}} \times 100$
* **Order Count:** $\text{DISTINCTCOUNT}(\text{OrderID})$
* **Units Sold:** $\sum\text{Quantity}$
* **Average Order Value (AOV):** $\frac{\text{Net Revenue}}{\text{Order Count}}$
* **Target Achievement %:** $\frac{\text{Actual Net Revenue}}{\text{Revenue Target}} \times 100$
* **YoY Growth %:** $\frac{\text{Current Period} - \text{Prior Year}}{\text{Prior Year}} \times 100$
