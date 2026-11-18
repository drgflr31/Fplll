import streamlit as st
import requests
@st.cache_data
def load_data():
    url="https://fantasy.premierleague.com/api/bootstrap-static/"
    response=requests.get(url)
    return response.json()
