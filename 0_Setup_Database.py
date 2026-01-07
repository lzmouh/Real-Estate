import streamlit as st
import subprocess
from db_health import db_exists_and_ready

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

You must build it using the Excel master file:
