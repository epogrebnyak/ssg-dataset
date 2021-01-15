import altair as alt
import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title="Static site generators dataset",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed",
)

url_csv = "https://raw.githubusercontent.com/epogrebnyak/ssg-dataset/main/data/ssg.csv"
url_metadata = (
    "https://raw.githubusercontent.com/epogrebnyak/ssg-dataset/main/data/metadata.json"
)


def pretty(s: str) -> str:
    try:
        return dict(js="JavaScript")[s]
    except KeyError:
        return s.capitalize()


@st.cache
def get_data():
    df = pd.read_csv(url_csv, parse_dates=["created", "modified"])
    df["lang"] = df.lang.map(pretty)
    return df


@st.cache
def get_meta():
    return requests.get(url_metadata).json()


_df = get_data()
meta = get_meta()
calver = "--".join(meta["created"].split("-"))

f"""
[![Download CSV](https://img.shields.io/badge/download-CSV-brightgreen)][url]
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4429834.svg)](https://doi.org/10.5281/zenodo.4429834)
![Release](https://img.shields.io/badge/release-{calver}-blue)
[![GitHub Repo stars](https://img.shields.io/github/stars/epogrebnyak/ssg-dataset?style=social)][gh]

[gh]: https://github.com/epogrebnyak/ssg-dataset
[url]: https://raw.githubusercontent.com/epogrebnyak/ssg-dataset/main/data/ssg.csv
"""

st.header("Static site generators popularity  :thermometer: :star:")


"""
Static site generators (SSG) are open source tools to create blogs, 
landing pages and documentation. 

[Hugo](https://gohugo.io/), 
[Gatsby](https://www.gatsbyjs.com/) and 
[Jekyll](https://jekyllrb.com/) 
are probably the most well-known SSG, but there are quite a few others
as described below. 
"""

st.header("Github stars")
"""
Number of stars in a Github repository is a proxy for SSG popularity, 
at least among developers. Surely many people can use a SSG without 
looking at the Github repo (by using the package repository and
consulting the homepage for download documentation), but the stars 
are quick available metric.
"""

# FIXME: should be able to reset as in https://discuss.streamlit.io/t/reset-multiselect-to-default-values-using-a-checkbox/1941
all_langs = _df.lang.unique().tolist()
langs = st.multiselect(
    "Programming languages", options=all_langs, default=all_langs, format_func=pretty
)
plot_df = _df[_df.lang.isin(langs)]
plot_df["stars"] = plot_df.stars.divide(1000).round(1)

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
            scale=alt.Scale(scheme="category10"),
        ),
        tooltip=["name", "stars", "lang"],
    )
)


st.altair_chart(chart, use_container_width=True)


st.header("Forks")
"""
Forks are copies of orginal repo made by users to submit code additions 
or to work on own version of the software. 
More forks indicate either active development of the package 
or code reuse in other projects.
"""

scatter = (
    alt.Chart(_df, title="Stars vs forks")
    .mark_circle(size=60)
    .encode(
        x="stars",
        y="forks",
        color="lang",
        tooltip=["name", "stars", "forks"],
    )
)

st.altair_chart(scatter, use_container_width=True)

"""
Consider there are two groups of SSG users: front-end engineers (FE),
usually proficient with HTML, CSS and JavaScript and non-specialised (NS) 
users who do other work (eg backend, data analysis or outside tech) 
and need to write a blog, lay out documentation or simple website.

More forks would come from FE group, while NS would likely to use the software 
as is and will not fork.

Distribution of project as an executable (Hugo), publishing pipeline (bookdown),
or indended audience (eleventy) may affect relative number of forks.

When project come to end-life - there would be more forks inteded to preserve
and continue to use it (Octopress).
"""

st.header("Open issues")

"""
More open issues in repository may be due to rapid project development or 
accumulated technical debt.
"""

ratios = _df.copy()
ratios["fork_ratio"] = (100 * ratios.forks / ratios.stars).round(2)
ratios["issues_ratio"] = (100 * ratios.open_issues / ratios.stars).round(2)

scale_down = st.checkbox("Zoom in", value=False)

if scale_down:
    plot_df2 = ratios[(ratios.issues_ratio < 10) & (ratios.fork_ratio < 30)]
else:
    plot_df2 = ratios

scatter2 = (
    alt.Chart(plot_df2, title="Open issues")
    .mark_circle()
    .encode(
        x=alt.X(
            "fork_ratio",
            title="Forks ÷ stars * 100%",
        ),
        y=alt.Y(
            "issues_ratio",
            title="Open issues ÷ stars * 100%",
        ),
        size=alt.Size("stars", legend=alt.Legend(title="Github stars")),
        color=alt.Color("lang", legend=alt.Legend(title="Language")),
        tooltip=["name", "stars", "forks"],
    )
)

st.altair_chart(scatter2, use_container_width=True)

st.header("Project lifetime")

"""
The longest-running static site generators are based on Ruby. 
The newest SSG are fastpages (Python) and Publish (Swift).
"""


def lapsed(x, today=meta["created"]):
    t = pd.to_datetime(today)
    return (t - x).days


t = _df.copy()
t["years"] = (t.modified - t.created).map(lambda x: x.days).divide(365).round(1)
t["silent"] = t.modified.map(lambda x: lapsed(x))
df = t.sort_values(["lang", "years"], ascending=[True, False])

ch = (
    alt.Chart(
        t.sort_values(["lang", "years"], ascending=[True, False]),
        title="Project lifetime",
    )
    .mark_bar()
    .encode(
        x=alt.X("years", title="Years"),
        y=alt.Y(
            "name",
            sort=alt.EncodingSortField(field="lang", order="ascending"),
            title="",
        ),
        color=alt.Color(
            "lang",
            legend=alt.Legend(title="Language"),
            scale=alt.Scale(scheme="tableau10"),
        ),
        tooltip=["name", "stars", "years"],
    )
)
st.altair_chart(ch, use_container_width=True)

"""
Several SSG are no longer maintained - one in Ruby, Python, and JavaScript.
"""
ch = (
    alt.Chart(
        t.sort_values("modified", ascending=True).head(3),
        title="Out of business",
    )
    .mark_bar()
    .encode(
        x=alt.X("silent", title="Days without commit"),
        y=alt.Y(
            "name",
            sort=alt.EncodingSortField(field="silent", order="descending"),
            title="",
        ),
        color=alt.Color(
            "lang",
            legend=alt.Legend(title="Language"),
            scale=alt.Scale(scheme="tableau10"),
        ),
        tooltip=["name", "stars", "years", "silent"],
    )
)
st.altair_chart(ch, use_container_width=True)

st.header("Links")

alpha = df.sort_values("name")
st.write(" - ".join(f"[{name}]({url})" for name, url in zip(alpha.name, alpha.url)))

st.header("Data")

f"""
[![](https://img.shields.io/badge/download-csv-brightgreen)]({url_csv})

Static CSV file [ssg.csv]({url_csv}) is prepared and posted via [epogrebnyak/ssg](https://github.com/epogrebnyak/ssg).

Dataset created on {meta["created"]}.

To download:

```python
import pandas as pd
url = "{url_csv}"
df = pd.read_csv(url_csv, parse_dates=["created", "modified"])
```
"""

st.dataframe(_df)

st.header("Citation")

"""
```
Evgeny Pogrebnyak. (2021). Github data for static site generators (SSG) popularity (Version 0.1.2) [Data set]. 
Zenodo. http://doi.org/10.5281/zenodo.4429834
```
"""

st.header("Contacts")

"""
[![Twitter Follow](https://img.shields.io/twitter/follow/PogrebnyakE?label=Follow&style=social)](https://twitter.com/PogrebnyakE)
[![MAIL Badge](https://img.shields.io/badge/-e.pogrebnyak@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:e.pogrebnyak@gmail.com)](mailto:e.pogrebnyak@gmail.com)

If you happen to have a good idea or comment about the dataset, please drop 
me a line. I appreciate the feedback and look forward to hearing about SSG
use cases, project development stories and applications of this dataset. 

(C) Evgeniy Pogrebnyak, 2021
"""
