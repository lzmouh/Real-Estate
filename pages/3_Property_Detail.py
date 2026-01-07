import streamlit as st
from database.db import get_session
from database.models import Property, Lease
from services.documents import save_document

#flat = st.selectbox("Select Property", [])
flat = st.session_state.get("selected_flat")
if not flat:
    st.warning("No property selected")
    st.stop()
    
db = get_session()
prop = db.query(Property).filter_by(flat=flat).first()
lease = db.query(Lease).filter_by(flat=flat).first()

st.header("Property Details")
st.write(prop.__dict__)

st.header("Lease Details")
st.write(lease.__dict__)

st.header("Documents")
file = st.file_uploader("Upload")
if file:
    save_document(flat, file)
    st.success("Uploaded")
