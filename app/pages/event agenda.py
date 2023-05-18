import streamlit as st
from bot import json_loader

st.snow()
st.title("Geektime Event Agenda")
st.table(json_loader(loc='agenda.json'))