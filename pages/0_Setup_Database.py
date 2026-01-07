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

st.warning("Database not found or incomplete")

st.markdown("""
### Setup Required
This application requires a populated database built from:

**Real estate Master.xlsx**
""")

if st.checkbox("I understand and want to build the database"):
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
            st.subheader("Error Output")
            st.code(result.stderr or result.stdout)