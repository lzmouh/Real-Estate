import os
import sqlite3

REQUIRED_TABLES = {
    "users",
    "properties",
    "owners",
    "tenants",
    "leases",
    "monthly_financials"
}

def db_exists_and_ready(db_path="database/real_estate.db"):
    if not os.path.exists(db_path):
        return False, "Database file does not exist"

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}
        conn.close()

        if not REQUIRED_TABLES.issubset(tables):
            return False, "Database exists but is missing required tables"

        return True, "Database is ready"

    except Exception as e:
        return False, str(e)
