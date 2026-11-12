# Deployment & Operations Guide

## 1. Prerequisites
* **Power BI Desktop** (November 2024 or later with PBIP and TMDL preview features enabled).
* **Power BI Pro, Premium Per User (PPU), or Fabric Capacity** for cloud workspace hosting.
* **Git** (version 2.40+) for source control.
* **Python 3.10+** (with `pandas` and `numpy`) for synthetic dataset generation and test execution.

---

## 2. Local Setup & Opening the Project

### Option A: Using the PBIP Git Project (Recommended)
1. Clone the repository:
   ```bash
   git clone https://github.com/Mahi-811/enterprise-sales-revenue-intelligence.git
   cd enterprise-sales-revenue-intelligence
   ```
2. Generate or refresh the processed dataset:
   ```bash
   python data/generate_data.py
   ```
3. Run the automated reconciliation test suite:
   ```bash
   python tests/test_reconciliation.py
   ```
4. Double-click `pbip/EnterpriseSalesIntelligence.pbip` to open directly in **Power BI Desktop**.
5. Power BI will read the TMDL semantic model, load table definitions, relationships, measures, and theme.
6. Click **Refresh** to pull data from `data/processed/`.

### Option B: Building a Fresh PBIX File via Power Query M
If your organization standardizes on classic `.pbix` files:
1. Open a blank **Power BI Desktop** session.
2. In the **Home** ribbon, click **Transform Data** to launch Power Query.
3. For each script in the `powerquery/` folder (`FactSales.m`, `FactTargets.m`, `DimDate.m`, etc.):
   - Click **New Source** &gt; **Blank Query**.
   - Open **Advanced Editor** and paste the contents of the respective `.m` file.
   - Rename the query to the table name.
4. Click **Close & Apply**.
5. Import `pbip/theme/executive_theme.json` via **View** &gt; **Themes** &gt; **Browse for themes**.
6. Create model relationships as documented in `docs/ARCHITECTURE.md`.
7. Import DAX measures from `dax/`.
8. Save as `EnterpriseSalesIntelligence.pbix`.

---

## 3. Relational SQL Deployment (PostgreSQL / SQL Server)
To deploy into a dedicated enterprise database rather than flat CSVs:
1. Connect to your SQL instance using `psql`, SSMS, or DBeaver.
2. Execute `sql/01_schema_ddl.sql` to establish tables, keys, and indexes.
3. Import the CSV files from `data/processed/` into the respective tables:
   ```sql
   -- Example PostgreSQL COPY command
   \copy DimTerritory FROM 'data/processed/DimTerritory.csv' WITH (FORMAT csv, HEADER true);
   \copy DimDate FROM 'data/processed/DimDate.csv' WITH (FORMAT csv, HEADER true);
   \copy DimCustomer FROM 'data/processed/DimCustomer.csv' WITH (FORMAT csv, HEADER true);
   \copy DimProduct FROM 'data/processed/DimProduct.csv' WITH (FORMAT csv, HEADER true);
   \copy DimSalesperson FROM 'data/processed/DimSalesperson.csv' WITH (FORMAT csv, HEADER true);
   \copy FactTargets FROM 'data/processed/FactTargets.csv' WITH (FORMAT csv, HEADER true);
   \copy FactSales FROM 'data/processed/FactSales.csv' WITH (FORMAT csv, HEADER true);
   ```
4. Run `sql/02_data_profiling.sql` to execute data quality checks.
5. Run `sql/04_reconciliation_kpis.sql` to verify that your SQL numbers match the reported DAX totals.

---

## 4. Power BI Service Publishing & Refresh Configuration

### Publishing to Workspace
1. In Power BI Desktop, click **File** &gt; **Publish** &gt; **Publish to Power BI**.
2. Select your target production or staging workspace (e.g., `Sales & Revenue BI [PROD]`).
3. Click **Select**.

### Gateway & Credentials Configuration
1. Open [Power BI Service](https://app.powerbi.com) in your web browser.
2. Navigate to your workspace &gt; locate the **EnterpriseSalesIntelligence** semantic model.
3. Click **Settings** (gear icon) &gt; **Data source credentials**.
4. Configure credentials (OAuth2 / Windows / Service Principal).
5. If using an on-premises database or shared file server, configure the **On-Premises Data Gateway**.

### Scheduled Refresh Schedule
1. Under semantic model settings, expand **Refresh**.
2. Toggle **Configure a refresh schedule** to **On**.
3. Configure refresh frequency (e.g., Daily at 06:00 AM UTC before business hours).
4. Enter notification email addresses to alert developers if a refresh fails.

---

## 5. Hosting the Live Interactive Web Preview via GitHub Pages
This repository includes a standalone client-side preview in `web_preview/`:
1. In your GitHub repository settings, go to **Pages** (under Code and automation).
2. Under **Build and deployment** &gt; **Source**, select **GitHub Actions**.
3. The included workflow `.github/workflows/deploy-pages.yml` will automatically build and publish the live dashboard to:
   `https://<username>.github.io/<repo-name>/`
