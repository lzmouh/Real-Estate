import streamlit as st
from database.db import get_session
from database.models import Property, User
from auth.auth import require_role

st.set_page_config(layout="wide")
st.title("🏢 Properties")

# --------------------------------------------------
# SECURITY CHECK
# --------------------------------------------------
if "user" not in st.session_state:
    st.error("You must be logged in")
    st.stop()

user = st.session_state.user
db = get_session()

# --------------------------------------------------
# LOAD PROPERTIES BASED ON ROLE
# --------------------------------------------------
if user.role == "admin":
    properties = db.query(Property).all()

elif user.role in ["owner", "tenant"]:
    # user.flat contains the linked flat number
    properties = db.query(Property).filter_by(flat=user.flat).all()

else:
    st.error("Invalid user role")
    st.stop()

# --------------------------------------------------
# DISPLAY PROPERTIES LIST
# --------------------------------------------------
if not properties:
    st.info("No properties available")
    st.stop()

st.subheader("Available Properties")

df = [
    {
        "Flat": p.flat,
        "Building": p.building_name,
        "Building No.": p.building_number,
        "Address": p.address,
        "Internet Provider": p.internet_provider,
        "Internet End": p.internet_end,
        "Property Cost": p.cost,
    }
    for p in properties
]

st.dataframe(df, use_container_width=True)

# --------------------------------------------------
# SELECT PROPERTY
# --------------------------------------------------
selected_flat = st.selectbox(
    "Select a property to view details",
    [p.flat for p in properties]
)

# --------------------------------------------------
# NAVIGATION TO DETAIL PAGE
# --------------------------------------------------
if st.button("View Property Details"):
    st.session_state.selected_flat = selected_flat
    st.switch_page("pages/3_Property_Detail.py")
