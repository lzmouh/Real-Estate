import pandas as pd
from sqlalchemy import create_engine
from passlib.hash import bcrypt
from datetime import datetime

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
EXCEL_FILE = "Real estate Master.xlsx"
DB_PATH = "sqlite:///database/real_estate.db"

engine = create_engine(DB_PATH, echo=False)

# -------------------------------------------------
# LOAD MASTER SHEET
# -------------------------------------------------
master = pd.read_excel(EXCEL_FILE, sheet_name="Master")

# -------------------------------------------------
# CLEAN COLUMN NAMES
# -------------------------------------------------
master.columns = master.columns.str.strip().str.lower().str.replace(" ", "_")

# -------------------------------------------------
# CREATE TABLES
# -------------------------------------------------
master_users = []
properties = []
owners = []
tenants = []
leases = []

for _, row in master.iterrows():
    flat = str(row["flat"])

    # -----------------------------
    # PROPERTIES
    # -----------------------------
    properties.append({
        "flat": flat,
        "building_name": row.get("building"),
        "building_number": row.get("building_no"),
        "address": row.get("address"),
        "parking": row.get("parking"),
        "internet_line": row.get("internet_line_number"),
        "internet_provider": row.get("internet"),
        "internet_end": row.get("internet_expiry"),
        "cost": row.get("capex")
    })

    # -----------------------------
    # OWNERS
    # -----------------------------
    owners.append({
        "flat": flat,
        "name": row.get("owner"),
        "address": row.get("address"),
        "id_number": None,
        "phone": row.get("phone"),
        "email": None
    })

    # -----------------------------
    # TENANTS
    # -----------------------------
    tenants.append({
        "flat": flat,
        "name": row.get("tenant"),
        "address": row.get("address"),
        "id_number": None,
        "phone": row.get("phone"),
        "email": None
    })

    # -----------------------------
    # LEASES
    # -----------------------------
    leases.append({
        "flat": flat,
        "start": row.get("lease_start"),
        "end": row.get("lease_end"),
        "rent": row.get("rent"),
        "allowance": row.get("ewa_limit")
    })

    # -----------------------------
    # USERS (OWNER + TENANT)
    # -----------------------------
    if pd.notna(row.get("owner")):
        master_users.append({
            "username": f"owner_{flat}",
            "password": bcrypt.hash("owner123"),
            "role": "owner",
            "flat": flat
        })

    if pd.notna(row.get("tenant")):
        master_users.append({
            "username": f"tenant_{flat}",
            "password": bcrypt.hash("tenant123"),
            "role": "tenant",
            "flat": flat
        })

# -------------------------------------------------
# WRITE TO DATABASE
# -------------------------------------------------
pd.DataFrame(properties).to_sql("properties", engine, if_exists="replace", index=False)
pd.DataFrame(owners).to_sql("owners", engine, if_exists="replace", index=False)
pd.DataFrame(tenants).to_sql("tenants", engine, if_exists="replace", index=False)
pd.DataFrame(leases).to_sql("leases", engine, if_exists="replace", index=False)

# -------------------------------------------------
# CREATE USERS TABLE
# -------------------------------------------------
users_df = pd.DataFrame(master_users)

admin = {
    "username": "admin",
    "password": bcrypt.hash("admin123"),
    "role": "admin",
    "flat": None
}

users_df = pd.concat([users_df, pd.DataFrame([admin])])
users_df.to_sql("users", engine, if_exists="replace", index=False)

# -------------------------------------------------
# MONTHLY FINANCIALS FROM FLAT SHEETS
# -------------------------------------------------
xls = pd.ExcelFile(EXCEL_FILE)

monthly_records = []

for sheet in xls.sheet_names:
    if sheet.lower() == "master":
        continue

    df = pd.read_excel(EXCEL_FILE, sheet_name=sheet)
    df.columns = df.columns.str.lower().str.strip()

    for _, r in df.iterrows():
        if pd.isna(r.get("month")):
            continue

        monthly_records.append({
            "flat": sheet,
            "month": r.get("month"),
            "rent": r.get("rent", 0),
            "taxes": 0,
            "ewa": r.get("ewa", 0),
            "ac": r.get("chiller", 0),
            "housekeeping": r.get("hk", 0),
            "internet": r.get("internet", 0),
            "management": r.get("management", 0),
            "misc": r.get("other", 0)
        })

if monthly_records:
    pd.DataFrame(monthly_records).to_sql(
        "monthly_financials", engine, if_exists="replace", index=False
    )

print("✅ real_estate.db successfully created from Excel")
