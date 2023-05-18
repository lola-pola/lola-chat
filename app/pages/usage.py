
import streamlit as st
from bot import json_loader
from bot import data

st.snow()
st.title("Geektime Event Usage Metrics")
st.table(json_loader(loc='results.json'))


st.bar_chart(json_loader(loc='results.json')
)
