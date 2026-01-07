import streamlit as st
import matplotlib.pyplot as plt
from services.calculations import roi

st.title("📊 Investment Performance")

income = st.number_input("Total Income")
spending = st.number_input("Total Spending")
cost = st.number_input("Property Cost")

st.metric("ROI %", roi(income, spending, cost))
