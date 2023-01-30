import altair as alt
import streamlit as st

from data import get_data, get_github_scale

_df = get_data()
n = len(_df)  # FIXME: can use n in badge, without generating local file

"""
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

all_langs = _df.lang.unique().tolist()


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
            scale=get_github_scale(),
        ),
        tooltip=["name", "stars", "lang"],
    )
)


st.altair_chart(chart, use_container_width=True)
