import os
import pandas as pd
from sqlalchemy import create_engine
from passlib.context import CryptContext

# -------------------------------------------------
# SAFETY & CONFIG
# -------------------------------------------------
os.makedirs("database", exist_ok=True)

EXCEL_FILE = "Real estate Master.xlsx"
DB_PATH = "sqlite:///database/real_estate.db"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

engine = create_engine(DB_PATH, echo=False)

# -------------------------------------------------
# LOAD MASTER SHEET
# -------------------------------------------------
master = pd.read_excel(EXCEL_FILE, sheet_name="Master")
master.columns = (
    master.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# -------------------------------------------------
# TABLE DATA
# -------------------------------------------------
properties, owners, tenants, leases, users = [], [], [], [], []

for _, row in master.iterrows():
    flat = str(row.get("flat")).strip()

    if not flat or flat == "nan":
        continue

    properties.append({
        "flat": flat,
        "building_name": row.get("building"),
        "building_number": row.get("building_no"),
        "address": row.get("address"),
        "parking": row.get("parking"),
        "internet_line": row.get("internet_line_number"),
        "internet_provider": row.get("internet"),
        "internet_end": row.get("internet_expiry"),
        "cost": row.get("capex"),
    })

    owners.append({
        "flat": flat,
        "name": row.get("owner"),
        "address": row.get("address"),
        "id_number": None,
        "phone": row.get("phone"),
        "email": None,
    })

    tenants.append({
        "flat": flat,
        "name": row.get("tenant"),
        "address": row.get("address"),
        "id_number": None,
        "phone": row.get("phone"),
        "email": None,
    })

    leases.append({
        "flat": flat,
        "start": row.get("lease_start"),
        "end": row.get("lease_end"),
        "rent": row.get("rent"),
        "allowance": row.get("ewa_limit"),
    })

    if pd.notna(row.get("owner")):
        users.append({
            "username": f"owner_{flat}",
            "password": pwd_context.hash("owner123"),
            "role": "owner",
            "flat": flat,
        })

    if pd.notna(row.get("tenant")):
        users.append({
            "username": f"tenant_{flat}",
            "password": pwd_context.hash("tenant123"),
            "role": "tenant",
            "flat": flat,
        })

# -------------------------------------------------
# ADMIN USER
# -------------------------------------------------
users.append({
    "username": "admin",
    "password": pwd_context.hash("admin123"),
    "role": "admin",
    "flat": None,
})

# -------------------------------------------------
# WRITE TABLES
# -------------------------------------------------
pd.DataFrame(properties).to_sql("properties", engine, if_exists="replace", index=False)
pd.DataFrame(owners).to_sql("owners", engine, if_exists="replace", index=False)
pd.DataFrame(tenants).to_sql("tenants", engine, if_exists="replace", index=False)
pd.DataFrame(leases).to_sql("leases", engine, if_exists="replace", index=False)
pd.DataFrame(users).to_sql("users", engine, if_exists="replace", index=False)

# -------------------------------------------------
# MONTHLY FINANCIALS FROM FLAT SHEETS
# -------------------------------------------------
xls = pd.ExcelFile(EXCEL_FILE)
monthly = []

for sheet in xls.sheet_names:
    if sheet.lower() == "master":
        continue

    df = pd.read_excel(EXCEL_FILE, sheet_name=sheet)
    df.columns = df.columns.str.lower().str.strip()

    for _, r in df.iterrows():
        if pd.isna(r.get("month")):
            continue

        monthly.append({
            "flat": sheet,
            "month": r.get("month"),
            "rent": r.get("rent", 0),
            "taxes": 0,
            "ewa": r.get("ewa", 0),
            "ac": r.get("chiller", 0),
            "housekeeping": r.get("hk", 0),
            "internet": r.get("internet", 0),
            "management": r.get("management", 0),
            "misc": r.get("other", 0),
        })

if monthly:
    pd.DataFrame(monthly).to_sql(
        "monthly_financials", engine, if_exists="replace", index=False
    )

print("✅ real_estate.db successfully built from Excel")