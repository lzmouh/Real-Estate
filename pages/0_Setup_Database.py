import streamlit as st
import subprocess
import sys
from utils.db_health import db_exists_and_ready

st.set_page_config(layout="wide")
st.title("🛠 Initial Database Setup")

ready, msg = db_exists_and_ready()

if ready:
    st.success("Database already initialized")
    st.stop()

st.warning("Real estate database not found or not initialized")

st.markdown("""
### Required action
This app needs a populated database built from:

**Real estate Master.xlsx**

The setup script will:
- Create all tables
- Import properties, owners, tenants
- Import monthly financials
""")

st.code("python build_db_from_excel.py")

if st.checkbox("I understand – run setup script now"):
    if st.button("🚀 Build Database"):
        with st.spinner("Building database..."):
            result = subprocess.run(
                [sys.executable, "build_db_from_excel.py"],
                capture_output=True,
                text=True
            )

        if result.returncode == 0:
            st.success("✅ Database built successfully")
            st.experimental_rerun()
        else:
            st.error("❌ Setup failed")
            st.subheader("Error output")
            st.code(result.stderr or result.stdout)