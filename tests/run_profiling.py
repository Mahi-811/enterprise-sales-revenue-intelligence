"""
Data Profiling & Quality Audit Execution Script
Loads raw staging CSV files into an in-memory SQLite database and executes
the data quality checks defined in sql/02_data_profiling.sql.
"""

import os
import sys
import sqlite3
import pandas as pd

# UTF-8 console output
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

def profile():
    print("=====================================================================")
    print("  Data Profiling & Anomaly Detection (SQLite In-Memory Engine)")
    print("=====================================================================")
    
    conn = sqlite3.connect(":memory:")
    
    # Load raw data
    raw_sales = pd.read_csv(os.path.join(RAW_DIR, "raw_sales_transactions.csv"))
    raw_sales.to_sql("stg_raw_sales", conn, index=False)
    
    # Load processed data
    for tbl in ["FactSales", "FactTargets", "DimCustomer", "DimProduct", "DimSalesperson", "DimTerritory", "DimDate"]:
        df = pd.read_csv(os.path.join(PROCESSED_DIR, f"{tbl}.csv"))
        df.to_sql(tbl, conn, index=False)
        
    cursor = conn.cursor()
    
    # 1. Anomaly detection in RAW
    cursor.execute("SELECT COUNT(*) FROM stg_raw_sales WHERE Quantity < 0")
    raw_negative_qty = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) - COUNT(DISTINCT OrderLineID) FROM stg_raw_sales")
    raw_duplicate_keys = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM stg_raw_sales s LEFT JOIN DimCustomer c ON s.CustomerKey = c.CustomerKey WHERE c.CustomerKey IS NULL")
    raw_orphan_cust = cursor.fetchone()[0]
    
    print(f"Raw Ingestion Anomaly Detection:")
    print(f"  - Detected Negative Quantities (Returns/Reversals): {raw_negative_qty}")
    print(f"  - Detected Duplicate OrderLineIDs: {raw_duplicate_keys}")
    print(f"  - Detected Orphan Customer Keys: {raw_orphan_cust}")
    
    # 2. Production FactSales verification
    cursor.execute("SELECT COUNT(*) FROM FactSales WHERE Quantity <= 0")
    prod_invalid_qty = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) - COUNT(DISTINCT OrderLineID) FROM FactSales")
    prod_duplicates = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM FactSales s LEFT JOIN DimCustomer c ON s.CustomerKey = c.CustomerKey WHERE c.CustomerKey IS NULL")
    prod_orphan_cust = cursor.fetchone()[0]
    
    print(f"\nProduction FactSales Cleansing Validation:")
    print(f"  - Production Invalid Quantities: {prod_invalid_qty} (Expected: 0)")
    print(f"  - Production Duplicate OrderLineIDs: {prod_duplicates} (Expected: 0)")
    print(f"  - Production Orphan Customer Keys: {prod_orphan_cust} (Expected: 0)")
    
    is_clean = (prod_invalid_qty == 0 and prod_duplicates == 0 and prod_orphan_cust == 0)
    print(f"\nProfiling Result: {'CLEAN - READY FOR PRODUCTION BI MODEL' if is_clean else 'FAILED'}")
    return is_clean

if __name__ == "__main__":
    success = profile()
    sys.exit(0 if success else 1)
