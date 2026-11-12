"""
Synthetic Data Generator for Enterprise Sales & Revenue Intelligence System
Conforms to SRS Document Version 1.0 (12 November 2026)
Generates:
  - DimDate (2024-01-01 to 2026-12-31)
  - DimTerritory (6 territories across 3 regions)
  - DimSalesperson (12 sales reps with managers & territory mappings)
  - DimProduct (32 products across 4 categories and 10 subcategories)
  - DimCustomer (80 enterprise/B2B/consumer customers)
  - FactSales (18,000+ transaction lines across 2024-2026)
  - FactTargets (Monthly targets by Salesperson & Territory)
  - UserSecurityMapping (Dynamic RLS mapping)
  - Raw staging data with controlled anomalies for profiling & ETL testing
"""

import os
import random
import datetime
import calendar
import pandas as pd
import numpy as np

# Set deterministic seed
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. DimTerritory
# -------------------------------------------------------------
territories_data = [
    {"TerritoryKey": 1, "TerritoryName": "North America East", "Region": "Americas", "Country": "United States"},
    {"TerritoryKey": 2, "TerritoryName": "North America West", "Region": "Americas", "Country": "United States"},
    {"TerritoryKey": 3, "TerritoryName": "Europe Central", "Region": "EMEA", "Country": "Germany"},
    {"TerritoryKey": 4, "TerritoryName": "Europe North & UK", "Region": "EMEA", "Country": "United Kingdom"},
    {"TerritoryKey": 5, "TerritoryName": "Asia Pacific East", "Region": "APAC", "Country": "Australia"},
    {"TerritoryKey": 6, "TerritoryName": "Latin America", "Region": "Americas", "Country": "Brazil"},
]
df_territory = pd.DataFrame(territories_data)

# -------------------------------------------------------------
# 2. DimSalesperson
# -------------------------------------------------------------
salespersons_data = [
    {"SalespersonKey": 1, "SalespersonID": "SP-001", "SalespersonName": "Sarah Jenkins", "Email": "sarah.jenkins@enterprisegroup.com", "Manager": "Marcus Vance", "TerritoryKey": 1},
    {"SalespersonKey": 2, "SalespersonID": "SP-002", "SalespersonName": "David Chen", "Email": "david.chen@enterprisegroup.com", "Manager": "Marcus Vance", "TerritoryKey": 1},
    {"SalespersonKey": 3, "SalespersonID": "SP-003", "SalespersonName": "Elena Rostova", "Email": "elena.rostova@enterprisegroup.com", "Manager": "Marcus Vance", "TerritoryKey": 2},
    {"SalespersonKey": 4, "SalespersonID": "SP-004", "SalespersonName": "Michael Scott", "Email": "michael.scott@enterprisegroup.com", "Manager": "Marcus Vance", "TerritoryKey": 2},
    {"SalespersonKey": 5, "SalespersonID": "SP-005", "SalespersonName": "Hans Gruber", "Email": "hans.gruber@enterprisegroup.com", "Manager": "Astrid Lindgren", "TerritoryKey": 3},
    {"SalespersonKey": 6, "SalespersonID": "SP-006", "SalespersonName": "Chloe Dupont", "Email": "chloe.dupont@enterprisegroup.com", "Manager": "Astrid Lindgren", "TerritoryKey": 3},
    {"SalespersonKey": 7, "SalespersonID": "SP-007", "SalespersonName": "Oliver Wright", "Email": "oliver.wright@enterprisegroup.com", "Manager": "Astrid Lindgren", "TerritoryKey": 4},
    {"SalespersonKey": 8, "SalespersonID": "SP-008", "SalespersonName": "Emma Watson", "Email": "emma.watson@enterprisegroup.com", "Manager": "Astrid Lindgren", "TerritoryKey": 4},
    {"SalespersonKey": 9, "SalespersonID": "SP-009", "SalespersonName": "Kenji Sato", "Email": "kenji.sato@enterprisegroup.com", "Manager": "Taro Tanaka", "TerritoryKey": 5},
    {"SalespersonKey": 10, "SalespersonID": "SP-010", "SalespersonName": "Priya Sharma", "Email": "priya.sharma@enterprisegroup.com", "Manager": "Taro Tanaka", "TerritoryKey": 5},
    {"SalespersonKey": 11, "SalespersonID": "SP-011", "SalespersonName": "Carlos Silva", "Email": "carlos.silva@enterprisegroup.com", "Manager": "Marcus Vance", "TerritoryKey": 6},
    {"SalespersonKey": 12, "SalespersonID": "SP-012", "SalespersonName": "Lucia Morales", "Email": "lucia.morales@enterprisegroup.com", "Manager": "Marcus Vance", "TerritoryKey": 6},
]
df_salesperson = pd.DataFrame(salespersons_data)

# -------------------------------------------------------------
# 3. DimProduct
# -------------------------------------------------------------
products_raw = [
    # Technology
    ("Apex Pro 16 Laptop", "Technology", "Laptops & Workstations", "ApexCore", 1150.00, 1850.00),
    ("Apex UltraBook 14", "Technology", "Laptops & Workstations", "ApexCore", 780.00, 1299.00),
    ("Zenith CAD Workstation", "Technology", "Laptops & Workstations", "Zenith", 1850.00, 2999.00),
    ("CloudScale Enterprise Server X1", "Technology", "Storage & Servers", "TitanCloud", 3200.00, 5200.00),
    ("Titan Dual Rack SAN 24TB", "Technology", "Storage & Servers", "TitanCloud", 2100.00, 3450.00),
    ("OmniSwitch 48-Port PoE+", "Technology", "Networking", "NetStream", 620.00, 1050.00),
    ("FiberLink Enterprise Gateway", "Technology", "Networking", "NetStream", 450.00, 780.00),
    ("Quantum 4K UHD Conference Display", "Technology", "Audio & Visual", "VisionTech", 890.00, 1499.00),
    
    # Office Solutions
    ("AeroMesh Ergonomic Task Chair", "Office Solutions", "Ergonomic Seating", "ErgoForm", 210.00, 399.00),
    ("Executive High-Back Leather Chair", "Office Solutions", "Ergonomic Seating", "ErgoForm", 320.00, 599.00),
    ("Vantage Motorized Sit-Stand Desk", "Office Solutions", "Executive Desks", "Vantage", 450.00, 850.00),
    ("Summit Modular Conference Table", "Office Solutions", "Executive Desks", "Vantage", 750.00, 1400.00),
    ("SteelLock 4-Drawer Fireproof Safe", "Office Solutions", "Storage Cabinets", "SafeGuard", 380.00, 680.00),
    ("SoundProof Modular Privacy Pod", "Office Solutions", "Workplace Acoustics", "QuietSpace", 2400.00, 4200.00),
    ("LaserMaster Heavy Duty Multifunction", "Office Solutions", "Printers & Scanners", "PrintCo", 520.00, 899.00),
    ("UltraClean Eco Office Shredder", "Office Solutions", "Printers & Scanners", "PrintCo", 140.00, 260.00),

    # Industrial & Hardware
    ("Heavy Duty Hydraulic Pallet Jack", "Industrial & Hardware", "Material Handling", "TorquePro", 280.00, 520.00),
    ("Electric Scissor Lift Platform", "Industrial & Hardware", "Material Handling", "TorquePro", 4100.00, 6900.00),
    ("ProTorq Industrial Cordless Drill Kit", "Industrial & Hardware", "Power Tools", "TorquePro", 130.00, 245.00),
    ("MaxVolt Brushless Rotary Hammer", "Industrial & Hardware", "Power Tools", "VoltWorks", 190.00, 360.00),
    ("MultiGas OSHA Air Quality Monitor", "Industrial & Hardware", "Safety Gear", "SafeGuard", 310.00, 580.00),
    ("ArcShield Auto-Darkening Welding Helmet", "Industrial & Hardware", "Safety Gear", "SafeGuard", 85.00, 160.00),
    ("Industrial Modular Tool Storage Cart", "Industrial & Hardware", "Storage Cabinets", "TorquePro", 480.00, 890.00),
    ("Precision Laser Measurement Suite", "Industrial & Hardware", "Inspection & Testing", "VoltWorks", 260.00, 490.00),

    # Consumables & Supplies
    ("Premium Multipurpose Laser Paper (Pallet)", "Consumables & Supplies", "Paper & Media", "PaperCraft", 350.00, 580.00),
    ("High-Yield Toner Cartridge Pack (CMYK)", "Consumables & Supplies", "Inks & Toners", "PrintCo", 180.00, 340.00),
    ("EcoGuard Industrial Shipping Wrap 6-Pack", "Consumables & Supplies", "Packaging", "EcoPack", 65.00, 120.00),
    ("Heavy Duty Corrugated Carton Pallet", "Consumables & Supplies", "Packaging", "EcoPack", 110.00, 195.00),
    ("Antimicrobial Surface Sanitizer Drum", "Consumables & Supplies", "Facilities", "CleanPro", 145.00, 275.00),
    ("Bulk Microfiber Cleaning Station Pack", "Consumables & Supplies", "Facilities", "CleanPro", 40.00, 85.00),
    ("Heavy-Duty Thermal Barcode Label Rolls", "Consumables & Supplies", "Paper & Media", "PaperCraft", 75.00, 140.00),
    ("Universal Power & Surge Tower 12-Outlets", "Consumables & Supplies", "Accessories", "VoltWorks", 32.00, 68.00)
]

products_data = []
for idx, p in enumerate(products_raw, start=1):
    products_data.append({
        "ProductKey": idx,
        "ProductID": f"PROD-{idx:03d}",
        "ProductName": p[0],
        "Category": p[1],
        "Subcategory": p[2],
        "Brand": p[3],
        "StandardCost": round(p[4], 2),
        "ListPrice": round(p[5], 2)
    })
df_product = pd.DataFrame(products_data)

# -------------------------------------------------------------
# 4. DimCustomer
# -------------------------------------------------------------
customer_names = [
    ("Nexus Global Logistics", "Corporate", "Chicago", "IL", "United States", "Americas", "2023-01-15"),
    ("Vanguard Aerospace Corp", "Corporate", "Seattle", "WA", "United States", "Americas", "2023-02-10"),
    ("Horizon Financial Partners", "Corporate", "New York", "NY", "United States", "Americas", "2023-03-01"),
    ("Summit Health Systems", "Enterprise B2B", "Boston", "MA", "United States", "Americas", "2023-04-18"),
    ("Pacific Marine Engineering", "Enterprise B2B", "San Francisco", "CA", "United States", "Americas", "2023-05-12"),
    ("Cascade Manufacturing", "Enterprise B2B", "Portland", "OR", "United States", "Americas", "2023-06-20"),
    ("Berlin Dynamics GmbH", "Corporate", "Berlin", "BE", "Germany", "EMEA", "2023-01-25"),
    ("Bavaria Precision AG", "Enterprise B2B", "Munich", "BY", "Germany", "EMEA", "2023-03-14"),
    ("Frankfurt Banking Solutions", "Corporate", "Frankfurt", "HE", "Germany", "EMEA", "2023-04-05"),
    ("London FinTech Labs", "Corporate", "London", "ENG", "United Kingdom", "EMEA", "2023-02-18"),
    ("Manchester Engineering Works", "Enterprise B2B", "Manchester", "ENG", "United Kingdom", "EMEA", "2023-07-09"),
    ("Edinburgh Digital Services", "Corporate", "Edinburgh", "SCT", "United Kingdom", "EMEA", "2023-08-11"),
    ("Sydney Infrastructure Group", "Corporate", "Sydney", "NSW", "Australia", "APAC", "2023-03-22"),
    ("Melbourne Tech Innovations", "Corporate", "Melbourne", "VIC", "Australia", "APAC", "2023-05-30"),
    ("Brisbane Resource Holdings", "Enterprise B2B", "Brisbane", "QLD", "Australia", "APAC", "2023-09-14"),
    ("Sao Paulo Logistica SA", "Enterprise B2B", "Sao Paulo", "SP", "Brazil", "Americas", "2023-04-10"),
    ("Rio Energia e Mineração", "Enterprise B2B", "Rio de Janeiro", "RJ", "Brazil", "Americas", "2023-06-15"),
    ("Curitiba Industrial Systems", "Corporate", "Curitiba", "PR", "Brazil", "Americas", "2023-10-01"),
]

# Add more to reach 80 customers across segments
segments = ["Corporate", "Enterprise B2B", "Consumer", "Home Office"]
cities = [
    ("Atlanta", "GA", "United States", "Americas"),
    ("Dallas", "TX", "United States", "Americas"),
    ("Denver", "CO", "United States", "Americas"),
    ("Hamburg", "HH", "Germany", "EMEA"),
    ("Stuttgart", "BW", "Germany", "EMEA"),
    ("Birmingham", "ENG", "United Kingdom", "EMEA"),
    ("Leeds", "ENG", "United Kingdom", "EMEA"),
    ("Perth", "WA", "Australia", "APAC"),
    ("Adelaide", "SA", "Australia", "APAC"),
    ("Belo Horizonte", "MG", "Brazil", "Americas"),
    ("Toronto", "ON", "Canada", "Americas"),
    ("Montreal", "QC", "Canada", "Americas"),
]

customers_data = []
for idx, c in enumerate(customer_names, start=1):
    customers_data.append({
        "CustomerKey": idx,
        "CustomerID": f"CUST-{idx:04d}",
        "CustomerName": c[0],
        "Segment": c[1],
        "City": c[2],
        "State": c[3],
        "Country": c[4],
        "Region": c[5],
        "AcquisitionDate": c[6]
    })

company_suffixes = ["Solutions", "Technologies", "Logistics", "Ventures", "Holdings", "Industries", "Group", "Global", "Enterprises", "Consulting"]
first_names = ["Robert", "Jennifer", "William", "Linda", "Richard", "Patricia", "Charles", "Barbara", "Thomas", "Elizabeth", "Daniel", "Susan", "Matthew", "Jessica", "Anthony", "Sarah"]
last_names = ["Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez"]

for i in range(len(customer_names) + 1, 81):
    seg = random.choices(segments, weights=[0.4, 0.3, 0.15, 0.15])[0]
    loc = random.choice(cities)
    if seg in ["Corporate", "Enterprise B2B"]:
        cname = f"{random.choice(last_names)} {random.choice(company_suffixes)}"
    else:
        cname = f"{random.choice(first_names)} {random.choice(last_names)}"
    
    # Acquisition dates spread between 2023-01-01 and 2025-06-30
    rand_days = random.randint(0, 900)
    acq_date = (datetime.date(2023, 1, 1) + datetime.timedelta(days=rand_days)).strftime("%Y-%m-%d")
    
    customers_data.append({
        "CustomerKey": i,
        "CustomerID": f"CUST-{i:04d}",
        "CustomerName": cname,
        "Segment": seg,
        "City": loc[0],
        "State": loc[1],
        "Country": loc[2],
        "Region": loc[3],
        "AcquisitionDate": acq_date
    })

df_customer = pd.DataFrame(customers_data)

# -------------------------------------------------------------
# 5. DimDate (2024-01-01 to 2026-12-31)
# -------------------------------------------------------------
date_rows = []
start_date = datetime.date(2024, 1, 1)
end_date = datetime.date(2026, 12, 31)
curr = start_date

while curr <= end_date:
    d_key = int(curr.strftime("%Y%m%d"))
    q = (curr.month - 1) // 3 + 1
    is_work = 1 if curr.weekday() < 5 else 0
    date_rows.append({
        "DateKey": d_key,
        "Date": curr.strftime("%Y-%m-%d"),
        "Year": curr.year,
        "Quarter": f"Q{q}",
        "YearQuarter": f"{curr.year}-Q{q}",
        "Month": curr.month,
        "MonthName": calendar.month_name[curr.month],
        "MonthShort": calendar.month_abbr[curr.month],
        "YearMonth": f"{curr.year}-{curr.month:02d}",
        "Week": int(curr.strftime("%U")) + 1,
        "DayOfWeek": curr.isoweekday(),
        "DayName": calendar.day_name[curr.weekday()],
        "IsWorkingDay": is_work
    })
    curr += datetime.timedelta(days=1)

df_date = pd.DataFrame(date_rows)

# -------------------------------------------------------------
# 6. FactTargets (Monthly target for 2024, 2025, 2026 up to Nov 2026)
# -------------------------------------------------------------
targets_data = []
target_id = 1

# Base target levels per salesperson with seasonal adjustments and yearly growth
base_monthly_targets = {
    1: 180000, 2: 150000, 3: 165000, 4: 140000,
    5: 195000, 6: 155000, 7: 175000, 8: 145000,
    9: 210000, 10: 160000, 11: 130000, 12: 125000
}

for year in [2024, 2025, 2026]:
    growth = 1.0 + (year - 2024) * 0.12 # 12% YoY growth in targets
    max_month = 12 if year < 2026 else 11 # up to November for current year 2026
    for m in range(1, max_month + 1):
        target_date = f"{year}-{m:02d}-01"
        target_period_key = int(f"{year}{m:02d}01")
        # Seasonality factor: Q4 peak, summer slight dip
        seasonal = 1.15 if m in [10, 11, 12] else (0.92 if m in [7, 8] else 1.0)
        
        for sp in salespersons_data:
            sp_key = sp["SalespersonKey"]
            t_key = sp["TerritoryKey"]
            base = base_monthly_targets[sp_key] * growth * seasonal
            # Add small random noise around targets
            rev_target = round(base * random.uniform(0.96, 1.04), -2)
            # Profit target approx 38-42% of revenue target
            prof_target = round(rev_target * random.uniform(0.38, 0.42), -2)
            
            targets_data.append({
                "TargetKey": target_id,
                "TargetDate": target_date,
                "DateKey": target_period_key,
                "YearMonth": f"{year}-{m:02d}",
                "TerritoryKey": t_key,
                "SalespersonKey": sp_key,
                "RevenueTarget": rev_target,
                "ProfitTarget": prof_target
            })
            target_id += 1

df_targets = pd.DataFrame(targets_data)

# -------------------------------------------------------------
# 7. FactSales Generation
# -------------------------------------------------------------
sales_rows = []
raw_sales_rows = [] # Raw with intentional anomalies
order_line_id = 1
order_id_counter = 10001

# Transaction generation period: 2024-01-01 to 2026-11-12
start_sim = datetime.date(2024, 1, 1)
end_sim = datetime.date(2026, 11, 12)
total_days = (end_sim - start_sim).days + 1

# Customer territory affinity
customer_territory_map = {}
for c in customers_data:
    reg = c["Region"]
    matching_terr = [t["TerritoryKey"] for t in territories_data if t["Region"] == reg]
    customer_territory_map[c["CustomerKey"]] = matching_terr

# Product key map for fast lookup
prod_lookup = {p["ProductKey"]: p for p in products_data}

current_day = start_sim
while current_day <= end_sim:
    # Day-of-week sales volume weighting
    dow = current_day.weekday()
    if dow >= 5: # Weekend
        num_orders = random.randint(3, 8)
    else: # Weekday
        # General growth trend over time
        day_idx = (current_day - start_sim).days
        trend_mult = 1.0 + (day_idx / total_days) * 0.28
        # Seasonal boost in Nov/Dec
        m_boost = 1.25 if current_day.month in [11, 12] else (0.90 if current_day.month in [7, 8] else 1.0)
        num_orders = int(random.randint(14, 25) * trend_mult * m_boost)
    
    date_key = int(current_day.strftime("%Y%m%d"))
    order_date_str = current_day.strftime("%Y-%m-%d")
    
    for _ in range(num_orders):
        order_id = f"ORD-{order_id_counter}"
        order_id_counter += 1
        
        # Pick customer
        cust_key = random.randint(1, len(customers_data))
        possible_territories = customer_territory_map.get(cust_key, [1])
        territory_key = random.choice(possible_territories)
        
        # Pick salesperson in that territory
        eligible_sp = [sp["SalespersonKey"] for sp in salespersons_data if sp["TerritoryKey"] == territory_key]
        if not eligible_sp:
            eligible_sp = [1]
        sp_key = random.choice(eligible_sp)
        
        # Order lines count (1 to 4 lines)
        lines_count = random.choices([1, 2, 3, 4], weights=[0.45, 0.30, 0.18, 0.07])[0]
        selected_prods = random.sample(list(prod_lookup.keys()), lines_count)
        
        for p_key in selected_prods:
            prod_info = prod_lookup[p_key]
            
            # Quantity depends on category (Consumables = bulk, Technology = lower units)
            cat = prod_info["Category"]
            if cat == "Consumables & Supplies":
                qty = random.choices([2, 5, 10, 20, 50], weights=[0.3, 0.35, 0.2, 0.1, 0.05])[0]
            elif cat == "Technology":
                qty = random.choices([1, 2, 3, 5, 10], weights=[0.55, 0.25, 0.12, 0.06, 0.02])[0]
            else:
                qty = random.choices([1, 2, 4, 8], weights=[0.5, 0.3, 0.15, 0.05])[0]
                
            unit_price = prod_info["ListPrice"]
            unit_cost = prod_info["StandardCost"]
            
            # Discount rate: mostly 0%, 5%, 10%, 15%, rarely 20%
            disc_rate = random.choices([0.0, 0.05, 0.10, 0.15, 0.20], weights=[0.50, 0.25, 0.15, 0.07, 0.03])[0]
            gross_line = round(unit_price * qty, 2)
            disc_amount = round(gross_line * disc_rate, 2)
            
            # Clean record for Processed Star Schema
            clean_record = {
                "OrderLineID": order_line_id,
                "OrderID": order_id,
                "OrderDate": order_date_str,
                "DateKey": date_key,
                "CustomerKey": cust_key,
                "ProductKey": p_key,
                "SalespersonKey": sp_key,
                "TerritoryKey": territory_key,
                "Quantity": qty,
                "UnitPrice": unit_price,
                "DiscountAmount": disc_amount,
                "UnitCost": unit_cost
            }
            sales_rows.append(clean_record)
            
            # Raw record can include raw attributes and raw anomalies
            raw_record = clean_record.copy()
            raw_sales_rows.append(raw_record)
            
            order_line_id += 1
            
    current_day += datetime.timedelta(days=1)

df_sales = pd.DataFrame(sales_rows)
df_raw_sales = pd.DataFrame(raw_sales_rows)

# Inject controlled anomalies into RAW data for testing Data Profiling & ETL rules:
# 1. Ten return records with negative quantities
for i in range(10):
    idx = random.randint(100, len(df_raw_sales) - 100)
    df_raw_sales.at[idx, "Quantity"] = -abs(int(df_raw_sales.at[idx, "Quantity"]))

# 2. Five duplicate order line IDs in raw
duplicate_rows = df_raw_sales.iloc[50:55].copy()
df_raw_sales = pd.concat([df_raw_sales, duplicate_rows], ignore_index=True)

# 3. Three orphan customer keys (e.g. 99999) in raw for profiling detection
for i in range(3):
    idx = random.randint(200, 300)
    df_raw_sales.at[idx, "CustomerKey"] = 99999

# -------------------------------------------------------------
# 8. UserSecurityMapping (Dynamic RLS)
# -------------------------------------------------------------
user_security_data = [
    {"UserEmail": "sarah.jenkins@enterprisegroup.com", "TerritoryKey": 1, "Role": "Sales Representative"},
    {"UserEmail": "david.chen@enterprisegroup.com", "TerritoryKey": 1, "Role": "Sales Representative"},
    {"UserEmail": "elena.rostova@enterprisegroup.com", "TerritoryKey": 2, "Role": "Sales Representative"},
    {"UserEmail": "michael.scott@enterprisegroup.com", "TerritoryKey": 2, "Role": "Sales Representative"},
    {"UserEmail": "marcus.vance@enterprisegroup.com", "TerritoryKey": 1, "Role": "Regional Manager Americas"},
    {"UserEmail": "marcus.vance@enterprisegroup.com", "TerritoryKey": 2, "Role": "Regional Manager Americas"},
    {"UserEmail": "marcus.vance@enterprisegroup.com", "TerritoryKey": 6, "Role": "Regional Manager Americas"},
    {"UserEmail": "astrid.lindgren@enterprisegroup.com", "TerritoryKey": 3, "Role": "Regional Manager EMEA"},
    {"UserEmail": "astrid.lindgren@enterprisegroup.com", "TerritoryKey": 4, "Role": "Regional Manager EMEA"},
    {"UserEmail": "taro.tanaka@enterprisegroup.com", "TerritoryKey": 5, "Role": "Regional Manager APAC"},
    {"UserEmail": "carlos.silva@enterprisegroup.com", "TerritoryKey": 6, "Role": "Sales Representative"},
    {"UserEmail": "lucia.morales@enterprisegroup.com", "TerritoryKey": 6, "Role": "Sales Representative"},
    {"UserEmail": "executive@enterprisegroup.com", "TerritoryKey": 0, "Role": "Executive Global Admin"}, # 0 denotes all
]
df_user_security = pd.DataFrame(user_security_data)

# -------------------------------------------------------------
# Save to Processed Directory (Clean Star Schema)
# -------------------------------------------------------------
df_sales.to_csv(os.path.join(PROCESSED_DIR, "FactSales.csv"), index=False)
df_targets.to_csv(os.path.join(PROCESSED_DIR, "FactTargets.csv"), index=False)
df_date.to_csv(os.path.join(PROCESSED_DIR, "DimDate.csv"), index=False)
df_customer.to_csv(os.path.join(PROCESSED_DIR, "DimCustomer.csv"), index=False)
df_product.to_csv(os.path.join(PROCESSED_DIR, "DimProduct.csv"), index=False)
df_salesperson.to_csv(os.path.join(PROCESSED_DIR, "DimSalesperson.csv"), index=False)
df_territory.to_csv(os.path.join(PROCESSED_DIR, "DimTerritory.csv"), index=False)
df_user_security.to_csv(os.path.join(PROCESSED_DIR, "UserSecurityMapping.csv"), index=False)

# Save to Raw Directory
df_raw_sales.to_csv(os.path.join(RAW_DIR, "raw_sales_transactions.csv"), index=False)
df_targets.to_csv(os.path.join(RAW_DIR, "raw_sales_targets.csv"), index=False)
df_customer.to_csv(os.path.join(RAW_DIR, "raw_customers.csv"), index=False)
df_product.to_csv(os.path.join(RAW_DIR, "raw_products.csv"), index=False)
df_salesperson.to_csv(os.path.join(RAW_DIR, "raw_salespersons.csv"), index=False)
df_territory.to_csv(os.path.join(RAW_DIR, "raw_territories.csv"), index=False)

print(f"Data generation complete.")
print(f"FactSales lines: {len(df_sales):,}")
print(f"FactTargets lines: {len(df_targets):,}")
print(f"DimDate rows: {len(df_date):,}")
print(f"DimCustomer rows: {len(df_customer):,}")
print(f"DimProduct rows: {len(df_product):,}")
print(f"DimSalesperson rows: {len(df_salesperson):,}")
print(f"DimTerritory rows: {len(df_territory):,}")
print(f"UserSecurityMapping rows: {len(df_user_security):,}")
print(f"Raw Sales with anomalies: {len(df_raw_sales):,}")
