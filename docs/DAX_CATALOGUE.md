# Enterprise DAX Measure Catalogue

This catalogue documents all explicit DAX business measures implemented within the **Enterprise Sales & Revenue Intelligence System**. Each measure is designed following best practices: strict separation of fact aggregation, reuse of atomic measures, safe division via `DIVIDE`, and optimized time intelligence against a marked calendar dimension.

---

## 1. Base Sales & Volume Measures

### Total Gross Sales
* **DAX Expression:**
  ```dax
  [Total Gross Sales] = 
  SUMX(
      FactSales,
      FactSales[Quantity] * FactSales[UnitPrice]
  )
  ```
* **Format:** `\$#,##0.00;(\$#,##0.00);"-"`
* **Description:** Iterates over sales lines to compute the undiscounted gross value before applying commercial line discounts.

### Total Discount Amount
* **DAX Expression:**
  ```dax
  [Total Discount Amount] = 
  SUM(FactSales[DiscountAmount])
  ```
* **Format:** `\$#,##0.00;(\$#,##0.00);"-"`
* **Description:** Sums the total dollar value of all line-level discounts granted.

### Total Net Revenue
* **DAX Expression:**
  ```dax
  [Total Net Revenue] = 
  [Total Gross Sales] - [Total Discount Amount]
  ```
* **Format:** `\$#,##0.00;(\$#,##0.00);"-"`
* **Description:** Core top-line financial revenue measure. Represents recognized net billing.

### Total Cost of Goods Sold (COGS)
* **DAX Expression:**
  ```dax
  [Total Cost of Goods Sold] = 
  SUMX(
      FactSales,
      FactSales[Quantity] * FactSales[UnitCost]
  )
  ```
* **Format:** `\$#,##0.00;(\$#,##0.00);"-"`
* **Description:** Evaluates aggregate standard inventory cost based on quantity sold and unit standard cost.

### Distinct Order Count
* **DAX Expression:**
  ```dax
  [Distinct Order Count] = 
  DISTINCTCOUNT(FactSales[OrderID])
  ```
* **Format:** `#,##0`
* **Description:** Counts unique orders placed. Prevents counting individual order lines as separate orders.

### Total Units Sold
* **DAX Expression:**
  ```dax
  [Total Units Sold] = 
  SUM(FactSales[Quantity])
  ```
* **Format:** `#,##0`
* **Description:** Total physical volume of goods delivered.

### Average Order Value (AOV)
* **DAX Expression:**
  ```dax
  [Average Order Value] = 
  DIVIDE(
      [Total Net Revenue],
      [Distinct Order Count],
      BLANK()
  )
  ```
* **Format:** `\$#,##0.00;(\$#,##0.00);"-"`
* **Description:** Average net revenue produced per customer purchase order.

---

## 2. Profitability & Margin Measures

### Total Gross Profit
* **DAX Expression:**
  ```dax
  [Total Gross Profit] = 
  [Total Net Revenue] - [Total Cost of Goods Sold]
  ```
* **Format:** `\$#,##0.00;(\$#,##0.00);"-"`
* **Description:** Net sales revenue remaining after direct cost of goods sold.

### Gross Margin %
* **DAX Expression:**
  ```dax
  [Gross Margin %] = 
  DIVIDE(
      [Total Gross Profit],
      [Total Net Revenue],
      BLANK()
  )
  ```
* **Format:** `0.0%`
* **Description:** Profitability ratio of gross profit to net revenue. Returns `BLANK()` if net revenue is zero.

### Cost Ratio %
* **DAX Expression:**
  ```dax
  [Cost Ratio %] = 
  DIVIDE(
      [Total Cost of Goods Sold],
      [Total Net Revenue],
      BLANK()
  )
  ```
* **Format:** `0.0%`
* **Description:** Percentage of revenue consumed by product cost. Satisfies: `Gross Margin % + Cost Ratio % = 100%`.

---

## 3. Time Intelligence Measures

### Revenue MTD / QTD / YTD
* **DAX Expressions:**
  ```dax
  [Revenue MTD] = TOTALMTD([Total Net Revenue], DimDate[Date])
  [Revenue QTD] = TOTALQTD([Total Net Revenue], DimDate[Date])
  [Revenue YTD] = TOTALYTD([Total Net Revenue], DimDate[Date])
  ```
* **Format:** `\$#,##0.00;(\$#,##0.00);"-"`
* **Description:** Cumulative period-to-date revenue calculations against continuous `DimDate`.

### Revenue Prior Year (PY)
* **DAX Expression:**
  ```dax
  [Revenue Prior Year (PY)] = 
  CALCULATE(
      [Total Net Revenue],
      SAMEPERIODLASTYEAR(DimDate[Date])
  )
  ```
* **Format:** `\$#,##0.00;(\$#,##0.00);"-"`
* **Description:** Revenue in the equivalent prior-year date window.

### Revenue YoY Growth %
* **DAX Expression:**
  ```dax
  [Revenue YoY Growth %] = 
  VAR CurrentRev = [Total Net Revenue]
  VAR PriorRev = [Revenue Prior Year (PY)]
  RETURN
  DIVIDE(CurrentRev - PriorRev, PriorRev, BLANK())
  ```
* **Format:** `+0.0%;-0.0%;"0.0%"`
* **Description:** Year-over-year percentage growth rate.

---

## 4. Quota & Target Attainment Measures

### Total Revenue Target
* **DAX Expression:**
  ```dax
  [Total Revenue Target] = 
  SUM(FactTargets[RevenueTarget])
  ```
* **Format:** `\$#,##0.00;(\$#,##0.00);"-"`
* **Description:** Quota targets aggregated from `FactTargets`.

### Revenue Target Attainment %
* **DAX Expression:**
  ```dax
  [Revenue Target Attainment %] = 
  DIVIDE(
      [Total Net Revenue],
      [Total Revenue Target],
      BLANK()
  )
  ```
* **Format:** `0.0%`
* **Description:** Actual net revenue divided by quota target. Values &ge; 100% signify quota achievement.

### Target Status Icon
* **DAX Expression:**
  ```dax
  [Target Status Icon] = 
  VAR Attainment = [Revenue Target Attainment %]
  RETURN
  SWITCH(
      TRUE(),
      ISBLANK(Attainment), "⚪ No Target",
      Attainment >= 1.05, "🟢 Overachieved (>105%)",
      Attainment >= 0.95, "🟢 On Target (95-105%)",
      Attainment >= 0.85, "🟡 At Risk (85-94%)",
      "🔴 Critical Gap (<85%)"
  )
  ```
* **Description:** Dynamic conditional indicator for matrix visuals and status cards.
