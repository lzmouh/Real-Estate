import streamlit as st
from db_health import db_exists_and_ready
from auth import authenticate

st.set_page_config(layout="wide")

ready, msg = db_exists_and_ready()

# --------------------------------------------------
# FIRST-TIME SETUP MODE
# --------------------------------------------------
if not ready:
    st.session_state.clear()
    st.switch_page("pages/0_Setup_Database.py")

# --------------------------------------------------
# NORMAL APP FLOW
# --------------------------------------------------
if "user" not in st.session_state:
    st.title("🔐 Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate(u, p)
        if user:
            st.session_state.user = user
            st.rerun()
        else:
            st.error("Invalid credentials")

else:
    st.sidebar.success(f"Logged in as {st.session_state.user.username}")
    st.sidebar.page_link("pages/1_Dashboard.py", label="Dashboard")
    st.sidebar.page_link("pages/2_Properties.py", label="Properties")
    st.sidebar.page_link("pages/4_Monthly_Statements.py", label="Statements")
    st.sidebar.page_link("pages/5_Reports.py", label="Reports")

    if st.session_state.user.role == "admin":
        st.sidebar.page_link("pages/6_Admin_Management.py", label="Admin")
