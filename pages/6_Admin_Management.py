import streamlit as st
from database.db import get_session
from database.models import Property

st.title("⚙️ Admin Management")

flat = st.text_input("Flat Number")
if st.button("Add Property"):
    db = get_session()
    db.add(Property(flat=flat))
    db.commit()
    st.success("Property Added")
