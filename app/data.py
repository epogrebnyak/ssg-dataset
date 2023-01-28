import pandas as pd
import requests
import streamlit as st

url_csv = "https://raw.githubusercontent.com/epogrebnyak/ssg-dataset/main/data/ssg.csv"
url_metadata = (
    "https://raw.githubusercontent.com/epogrebnyak/ssg-dataset/main/data/metadata.json"
)


@st.cache
def get_data():
    return pd.read_csv(url_csv, parse_dates=["created", "modified"])


@st.cache
def get_meta():
    return requests.get(url_metadata).json()


st.session_state['df'] = get_data()
st.session_state['meta'] = get_meta()
st.session_state['url_csv'] = url_csv
