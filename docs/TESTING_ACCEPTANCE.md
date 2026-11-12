# Testing & Acceptance Verification Guide

## 1. Testing Strategy
Testing of the **Enterprise Sales & Revenue Intelligence System** validates data completeness, referential integrity, business logic accuracy, time-intelligence calculations, and security isolation across both tabular and visual layers.

---

## 2. Acceptance Criteria Matrix
| Criterion ID | Requirement Statement | Verification Method | Status |
| :--- | :--- | :--- | :--- |
| **AC-01** | All required source tables load without unexplained errors. | Automated table ingestion test. | **PASS** |
| **AC-02** | `FactSales` has unique order-line key and valid dimension references. | Primary key & orphan foreign key audit. | **PASS** |
| **AC-03** | Revenue, cost, gross profit, orders, units, and margin reconcile to ground-truth. | Automated SQL vs Python vs DAX reconciliation. | **PASS** |
| **AC-04** | Time-intelligence measures return correct results for selected and prior periods. | Prior-year comparison & YoY growth audit. | **PASS** |
| **AC-05** | Target grain uniqueness and actual vs target quota attainment calculation. | Multi-column target key deduplication check. | **PASS** |
| **AC-06** | Dimensional hierarchies filter all intended facts without data loss. | Cross-dimensional summation verification. | **PASS** |
| **AC-07** | Row-Level Security (RLS) restricts data for each test identity as designed. | Identity impersonation verification. | **PASS** |
| **AC-08** | Business plausibility rules (non-negative price, cost, discount <= gross). | Range and logical constraint check. | **PASS** |
| **AC-09** | Repository includes reproducible project assets and setup documentation. | Deliverables file verification. | **PASS** |

---

## 3. Test Cases (TC-01 through TC-08)

### TC-01: Calendar Year Slicer Filter
* **Action:** Select calendar year `2025` on slicer.
* **Expected Result:** Visual cards update to show 2025 Net Revenue (\$32,755,256.25) and margin (39.36%).
* **Actual Result:** Reconciles perfectly to ground truth.

### TC-02: Regional Dimension Isolation
* **Action:** Select region `EMEA`.
* **Expected Result:** Total Net Revenue displays \$31,247,910.75 across Europe Central and Europe North territories.
* **Actual Result:** Matches database subset with zero variance.

### TC-03: Prior Year (YoY) Comparison
* **Action:** Compare 2025 vs 2024 performance.
* **Expected Result:** Net Revenue increases from \$30,822,415.00 to \$32,755,256.25, showing YoY growth of +6.27%.
* **Actual Result:** Confirmed across both SQL and DAX models.

### TC-04: Product Category Drill-Down
* **Action:** Select `Technology` category and drill down to product SKU level.
* **Expected Result:** Sum of individual technology products exactly equals the Technology category total.
* **Actual Result:** 100% additive reconciliation.

### TC-05: Drill-Through to Transaction Detail
* **Action:** Right-click on product `Apex Pro 16 Laptop` and select "Drill-through to RP-06 Transaction Detail".
* **Expected Result:** Filter context preserved, showing only order lines for that SKU.
* **Actual Result:** Drill-through filter active and context preserved.

### TC-06: Territory Security Boundary Check
* **Action:** Test View As `marcus.vance@enterprisegroup.com` (Americas).
* **Expected Result:** EMEA and APAC territories hidden; only Americas data visible.
* **Actual Result:** Security table filter restricts facts to Territories 1, 2, and 6.

### TC-07: Raw Duplicate & Anomaly Ingestion
* **Action:** Ingest raw CSV containing 5 duplicate lines and 10 negative return quantities.
* **Expected Result:** Profiling script flags anomalies; production ETL deduplicates and quarantines.
* **Actual Result:** Profiling audit flags 10 returns and 5 duplicates in raw; production table has 0 duplicates.

### TC-08: Empty State Handling
* **Action:** Apply mutually exclusive slicers with no matching sales.
* **Expected Result:** Visual shows clear empty-state message rather than misleading zeros or errors.
* **Actual Result:** Handled via `[Empty State Message]` measure.
