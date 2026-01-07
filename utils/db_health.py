import os
import sqlite3

REQUIRED_TABLES = {
    "users",
    "properties",
    "owners",
    "tenants",
    "leases",
    "monthly_financials",
}

def db_exists_and_ready(db_path="database/real_estate.db"):
    if not os.path.exists(db_path):
        return False, "Database file missing"

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {r[0] for r in cur.fetchall()}
        conn.close()

        if not REQUIRED_TABLES.issubset(tables):
            return False, "Missing required tables"

        return True, "Database ready"
    except Exception as e:
        return False, str(e)