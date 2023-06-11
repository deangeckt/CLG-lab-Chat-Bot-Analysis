import streamlit as st


st.set_page_config(page_title="Aggregations", page_icon="📊", layout="wide")
st.sidebar.success("Aggregations")

st.write("Aggregations ")

st.markdown(
    """ Aggregations stuff
"""
)

option = st.selectbox('Choose data source', ('Email', 'Home phone', 'Mobile phone'))
