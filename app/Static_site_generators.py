import altair as alt
import pandas as pd
import requests
import streamlit as st

url_csv = "https://raw.githubusercontent.com/epogrebnyak/ssg-dataset/main/data/ssg.csv"


@st.cache
def get_data():
    return pd.read_csv(url_csv, parse_dates=["created", "modified"])


st.session_state["df"] = get_data()
st.session_state["url_csv"] = url_csv

_df = st.session_state["df"]
n = len(_df) # FIXME: can use n in badge, without generating local file

f"""
[gh]: https://github.com/epogrebnyak/ssg-dataset
[url]: https://raw.githubusercontent.com/epogrebnyak/ssg-dataset/main/data/ssg.csv
![count](https://raw.githubusercontent.com/epogrebnyak/ssg-dataset/main/app/ssg_count.svg)
[![Download CSV](https://img.shields.io/badge/download-CSV-brightgreen)][url]
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4429834.svg)](https://doi.org/10.5281/zenodo.4429834)
![release](https://badgen.net/github/release/epogrebnyak/ssg-dataset)
[![GitHub Repo stars](https://img.shields.io/github/stars/epogrebnyak/ssg-dataset?style=social)][gh]
"""


st.header("Static site generators popularity  :thermometer: :star:")

"""
Static site generators (SSG) are open source tools to create blogs, 
landing pages and documentation. 

[Hugo](https://gohugo.io/), 
[Gatsby](https://www.gatsbyjs.com/) and 
[Jekyll](https://jekyllrb.com/) 
are probably the most well-known SSG, but there are quite a few others. 
"""

st.header("Github stars")
"""
Number of stars in a Github repository is a proxy for SSG popularity, 
at least among software developers.
"""

# FIXME: should be able to reset as in https://discuss.streamlit.io/t/reset-multiselect-to-default-values-using-a-checkbox/1941
all_langs = _df.lang.unique().tolist()


@st.cache
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


col_keys, col_values = palette(all_langs)
github_scale = alt.Scale(domain=col_keys, range=col_values)
st.session_state["github_scale"] = github_scale


selected_langs = st.multiselect(
    "Programming languages", options=all_langs, default=all_langs
)
plot_df = _df[_df.lang.isin(selected_langs)]
plot_df["stars"] = plot_df.stars.divide(1000).round(1)

# https://altair-viz.github.io/user_guide/customization.html#raw-color-values

chart = (
    alt.Chart(
        plot_df,
        title="Static site generators popularity",
    )
    .mark_bar()
    .encode(
        x=alt.X("stars", title="'000 stars on Github"),
        y=alt.Y(
            "name",
            sort=alt.EncodingSortField(field="stars", order="descending"),
            title="",
        ),
        color=alt.Color(
            "lang",
            legend=alt.Legend(title="Language"),
            scale=github_scale,
        ),
        tooltip=["name", "stars", "lang"],
    )
)


st.altair_chart(chart, use_container_width=True)
