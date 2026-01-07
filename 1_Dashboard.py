import streamlit as st
from database.db import get_session
from database.models import Property

st.title("🏠 Portfolio Summary")

db = get_session()
props = db.query(Property).all()

st.metric("Total Properties", len(props))
st.dataframe([{p.flat: p.building_name} for p in props])
