import streamlit as st
from services.calculations import allowance_excess

st.title("📅 Monthly Statement")

ewa = st.number_input("EWA")
ac = st.number_input("AC")
allowance = st.number_input("Allowance")

st.metric("Allowance Excess", allowance_excess(ewa, ac, allowance))
