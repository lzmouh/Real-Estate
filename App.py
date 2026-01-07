import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import hashlib
from datetime import date, datetime, timedelta
from passlib.hash import bcrypt
import matplotlib.pyplot as plt

# =============================
# CONFIG
# =============================
st.set_page_config(page_title="Real Estate Management", layout="wide")

DB = "real_estate.db"

# =============================
# DATABASE
# =============================
def get_conn():
    return sqlite3.connect(DB, check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT,
        linked_property TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS properties (
        flat TEXT PRIMARY KEY,
        building_name TEXT,
        building_number TEXT,
        address TEXT,
        parking TEXT,
        internet_line TEXT,
        internet_provider TEXT,
        internet_end DATE,
        property_cost REAL
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS owners (
        flat TEXT,
        name TEXT,
        address TEXT,
        id_number TEXT,
        phone TEXT,
        email TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS tenants (
        flat TEXT,
        name TEXT,
        address TEXT,
        id_number TEXT,
        phone TEXT,
        email TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS leases (
        flat TEXT,
        start DATE,
        end DATE,
        rent REAL,
        allowance REAL
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS monthly_financials (
        flat TEXT,
        month TEXT,
        rent REAL,
        taxes REAL,
        ewa REAL,
        ac REAL,
        housekeeping REAL,
        internet REAL,
        management REAL,
        misc REAL
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS maintenance (
        flat TEXT,
        anniversary DATE,
        amount REAL
    )
    """)

    conn.commit()
    conn.close()

init_db()

# =============================
# AUTH
# =============================
def login(username, password):
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM users WHERE username=?", conn, params=(username,))
    conn.close()

    if not df.empty and bcrypt.verify(password, df.iloc[0]["password"]):
        return df.iloc[0].to_dict()
    return None

def create_user(username, password, role, flat=None):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO users VALUES (NULL,?,?,?,?)",
        (username, bcrypt.hash(password), role, flat)
    )
    conn.commit()
    conn.close()

# =============================
# UTILITIES
# =============================
def role_required(roles):
    if st.session_state["user"]["role"] not in roles:
        st.error("Access denied")
        st.stop()

def calculate_excess(ewa, ac, allowance):
    return max((ewa + ac) - allowance, 0)

# =============================
# PAGES
# =============================
def login_page():
    st.title("🔐 Real Estate Management Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login(u, p)
        if user:
            st.session_state["user"] = user
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

def dashboard():
    st.title("🏠 Portfolio Overview")

    conn = get_conn()
    df = pd.read_sql("SELECT * FROM properties", conn)
    conn.close()

    st.metric("Total Properties", len(df))
    st.dataframe(df)

def property_page(flat):
    st.title(f"🏢 Property {flat}")

    conn = get_conn()
    prop = pd.read_sql("SELECT * FROM properties WHERE flat=?", conn, params=(flat,))
    owner = pd.read_sql("SELECT * FROM owners WHERE flat=?", conn, params=(flat,))
    tenant = pd.read_sql("SELECT * FROM tenants WHERE flat=?", conn, params=(flat,))
    lease = pd.read_sql("SELECT * FROM leases WHERE flat=?", conn, params=(flat,))
    conn.close()

    # SECTION 1
    st.header("Property Details")
    st.json(prop.to_dict(orient="records")[0])

    # SECTION 2
    st.header("Owner Details")
    st.json(owner.to_dict(orient="records")[0])

    # SECTION 3
    st.header("Tenant & Lease")
    st.json(tenant.to_dict(orient="records")[0])
    st.json(lease.to_dict(orient="records")[0])

    # SECTION 4
    st.header("Documents")
    st.file_uploader("Upload documents", accept_multiple_files=True)

def monthly_statement(flat):
    st.title(f"📅 Monthly Statement – {flat}")

    conn = get_conn()
    df = pd.read_sql("SELECT * FROM monthly_financials WHERE flat=?", conn, params=(flat,))
    lease = pd.read_sql("SELECT allowance FROM leases WHERE flat=?", conn, params=(flat,))
    conn.close()

    df["excess"] = df.apply(
        lambda r: calculate_excess(r.ewa, r.ac, lease.iloc[0]["allowance"]), axis=1
    )

    role = st.session_state["user"]["role"]

    if role == "admin":
        st.data_editor(df, num_rows="dynamic")
    elif role == "owner":
        st.dataframe(df)
    else:
        st.dataframe(df[["month", "rent", "ewa", "ac", "excess"]])

def reports():
    st.title("📊 Investment Performance")

    conn = get_conn()
    fin = pd.read_sql("SELECT * FROM monthly_financials", conn)
    props = pd.read_sql("SELECT * FROM properties", conn)
    conn.close()

    fin["total_income"] = fin["rent"] + fin["taxes"]
    fin["total_spending"] = fin[["ewa","ac","housekeeping","internet","management","misc"]].sum(axis=1)

    summary = fin.groupby("flat").sum().reset_index()
    summary = summary.merge(props[["flat","property_cost"]], on="flat")

    summary["ROI"] = (summary["total_income"] - summary["total_spending"]) / summary["property_cost"] * 100

    st.dataframe(summary)

    f1, f2 = st.selectbox("Flat 1", summary.flat), st.selectbox("Flat 2", summary.flat)
    st.bar_chart(summary.set_index("flat").loc[[f1,f2]][["total_income","total_spending"]])

# =============================
# NAVIGATION
# =============================
if "user" not in st.session_state:
    login_page()
else:
    role = st.session_state["user"]["role"]

    menu = ["Dashboard","Reports","Logout"]
    if role == "admin":
        menu.insert(1,"Manage Properties")

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Dashboard":
        dashboard()

    elif choice == "Reports":
        reports()

    elif choice == "Logout":
        del st.session_state["user"]
        st.experimental_rerun()
