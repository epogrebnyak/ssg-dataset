import altair as alt
import pandas as pd
import requests
import streamlit as st

url_csv = "https://raw.githubusercontent.com/epogrebnyak/ssg-dataset/main/data/ssg.csv"


@st.experimental_memo
def get_data():
    return pd.read_csv(url_csv, parse_dates=["created", "modified"])


@st.experimental_memo
def palette(languages, default_color="#BEBEBE"):
    r = requests.get(
        "https://raw.githubusercontent.com/ozh/github-colors/master/colors.json"
    ).json()
    pal = {}
    for lang in languages:
        try:
            pal[lang] = r[lang]["color"]
        except KeyError:
            pal[lang] = default_color
    return list(pal.keys()), list(pal.values())


def get_github_scale():
    all_langs = get_data().lang.unique().tolist()
    col_keys, col_values = palette(all_langs)
    github_scale = alt.Scale(domain=col_keys, range=col_values)
    return github_scale
