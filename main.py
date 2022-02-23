from data_visual_runner import data_plot
from data_set_runner import data_set
from header import print_header
import streamlit as st

print_header()
operations = ['Data lookup' , 'Data plot']
operation = st.selectbox("Please select the operation", operations)
if operation == 'Data lookup':
    data_set()
else:
    data_plot()