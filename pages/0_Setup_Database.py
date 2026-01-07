import streamlit as st
import subprocess
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
This application requires a populated **real_estate.db** file.

You must build it using the Excel master file.
The script will:
- Read all flats
- Create users, properties, leases
- Import monthly financials
""")

st.code("python build_db_from_excel.py")

st.info("⚠️ Make sure Excel file is in the project root")

# OPTIONAL SAFE EXECUTION
if st.checkbox("I understand – run setup script now"):
    if st.button("🚀 Build Database"):
        try:
            subprocess.run(
                ["python", "build_db_from_excel.py"],
                check=True
            )
            st.success("Database built successfully")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Setup failed: {e}")
