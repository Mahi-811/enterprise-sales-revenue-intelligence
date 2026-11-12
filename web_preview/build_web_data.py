"""
Pre-aggregates and generates web_preview/data.json for instant client-side rendering.
Contains:
  - Global KPI summary
  - Monthly time-series (Revenue, Target, Profit, Orders)
  - Regional & Territory breakdown
  - Product Category and Top/Bottom Products breakdown
  - Salesperson rankings & target attainment
  - Customer Segment distribution & top customers
  - Sample transaction lines for RP-06 Transaction Detail table
"""

import os
import json
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
WEB_DIR = os.path.join(BASE_DIR, "web_preview")
os.makedirs(WEB_DIR, exist_ok=True)

df_sales = pd.read_csv(os.path.join(DATA_DIR, "FactSales.csv"))
df_targets = pd.read_csv(os.path.join(DATA_DIR, "FactTargets.csv"))
df_date = pd.read_csv(os.path.join(DATA_DIR, "DimDate.csv"))
df_cust = pd.read_csv(os.path.join(DATA_DIR, "DimCustomer.csv"))
df_prod = pd.read_csv(os.path.join(DATA_DIR, "DimProduct.csv"))
df_sp = pd.read_csv(os.path.join(DATA_DIR, "DimSalesperson.csv"))
df_terr = pd.read_csv(os.path.join(DATA_DIR, "DimTerritory.csv"))

# Merge master analytical frame
df = df_sales.merge(df_date[["DateKey", "Year", "YearMonth", "Quarter"]], on="DateKey")
df = df.merge(df_terr[["TerritoryKey", "TerritoryName", "Region"]], on="TerritoryKey")
df = df.merge(df_prod[["ProductKey", "ProductName", "Category", "Subcategory"]], on="ProductKey")
df = df.merge(df_sp[["SalespersonKey", "SalespersonName"]], on="SalespersonKey")
df = df.merge(df_cust[["CustomerKey", "CustomerName", "Segment"]], on="CustomerKey")

df["GrossSales"] = df["Quantity"] * df["UnitPrice"]
df["NetRevenue"] = df["GrossSales"] - df["DiscountAmount"]
df["COGS"] = df["Quantity"] * df["UnitCost"]
df["GrossProfit"] = df["NetRevenue"] - df["COGS"]

# Monthly series
monthly = df.groupby(["YearMonth", "Region", "Category"]).agg(
    Revenue=("NetRevenue", "sum"),
    Profit=("GrossProfit", "sum"),
    GrossSales=("GrossSales", "sum"),
    COGS=("COGS", "sum"),
    Orders=("OrderID", "nunique"),
    Units=("Quantity", "sum")
).reset_index()

# Monthly targets
target_monthly = df_targets.merge(df_terr[["TerritoryKey", "Region"]], on="TerritoryKey").groupby(
    ["YearMonth", "Region"]
).agg(
    RevenueTarget=("RevenueTarget", "sum"),
    ProfitTarget=("ProfitTarget", "sum")
).reset_index()

# Top products
prod_perf = df.groupby(["ProductID", "ProductName", "Category"] if "ProductID" in df else ["ProductKey", "ProductName", "Category"]).agg(
    Revenue=("NetRevenue", "sum"),
    Profit=("GrossProfit", "sum"),
    Units=("Quantity", "sum"),
    Orders=("OrderID", "nunique")
).reset_index()
prod_perf["MarginPct"] = (prod_perf["Profit"] / prod_perf["Revenue"] * 100).round(2)
prod_perf = prod_perf.sort_values(by="Revenue", ascending=False)

# Salesperson performance
sp_perf = df.groupby(["SalespersonKey", "SalespersonName", "Region"]).agg(
    Revenue=("NetRevenue", "sum"),
    Profit=("GrossProfit", "sum"),
    Orders=("OrderID", "nunique")
).reset_index()
sp_targets = df_targets.groupby("SalespersonKey").agg(TargetRevenue=("RevenueTarget", "sum")).reset_index()
sp_perf = sp_perf.merge(sp_targets, on="SalespersonKey")
sp_perf["AttainmentPct"] = (sp_perf["Revenue"] / sp_perf["TargetRevenue"] * 100).round(2)
sp_perf = sp_perf.sort_values(by="Revenue", ascending=False)

# Customer Segment performance
seg_perf = df.groupby("Segment").agg(
    Revenue=("NetRevenue", "sum"),
    Profit=("GrossProfit", "sum"),
    Customers=("CustomerKey", "nunique"),
    Orders=("OrderID", "nunique")
).reset_index()

# Sample 150 transaction rows for RP-06
sample_tx = df.sort_values(by="OrderDate", ascending=False).head(150)[[
    "OrderLineID", "OrderID", "OrderDate", "CustomerName", "ProductName", 
    "Category", "SalespersonName", "Region", "Quantity", "UnitPrice", 
    "DiscountAmount", "NetRevenue", "GrossProfit"
]].to_dict(orient="records")

payload = {
    "summary": {
        "grossSales": round(df["GrossSales"].sum(), 2),
        "discounts": round(df["DiscountAmount"].sum(), 2),
        "netRevenue": round(df["NetRevenue"].sum(), 2),
        "cogs": round(df["COGS"].sum(), 2),
        "grossProfit": round(df["GrossProfit"].sum(), 2),
        "marginPct": round((df["GrossProfit"].sum() / df["NetRevenue"].sum()) * 100, 2),
        "orderCount": int(df["OrderID"].nunique()),
        "unitsSold": int(df["Quantity"].sum()),
        "aov": round(df["NetRevenue"].sum() / df["OrderID"].nunique(), 2),
        "targetRevenue": round(df_targets["RevenueTarget"].sum(), 2),
        "targetAttainmentPct": round((df["NetRevenue"].sum() / df_targets["RevenueTarget"].sum()) * 100, 2),
        "activeCustomers": int(df["CustomerKey"].nunique()),
        "lastRefresh": "2026-11-12 18:00:00 UTC"
    },
    "monthly": monthly.to_dict(orient="records"),
    "targets": target_monthly.to_dict(orient="records"),
    "products": prod_perf.to_dict(orient="records"),
    "salespersons": sp_perf.to_dict(orient="records"),
    "segments": seg_perf.to_dict(orient="records"),
    "recentTransactions": sample_tx
}

with open(os.path.join(WEB_DIR, "data.json"), "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2)

print(f"web_preview/data.json generated successfully. Size: {os.path.getsize(os.path.join(WEB_DIR, 'data.json')) / 1024:.1f} KB")
