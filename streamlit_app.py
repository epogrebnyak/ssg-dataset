import altair as alt
import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title="Github data on static site generators (SSG)",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed",
)

url_csv = "https://raw.githubusercontent.com/epogrebnyak/ssg/main/data/ssg.csv"
url_metadata = "https://raw.githubusercontent.com/epogrebnyak/ssg/main/data/metadata.json"

def pretty(s: str) -> str:
    try:
        return dict(js="JavaScript")[s]
    except KeyError:
        return s.capitalize()


@st.cache
def get_data():
    df = pd.read_csv(url_csv)
    df["lang"] = df.lang.map(pretty)
    return df

@st.cache
def get_meta():
    return requests.get(url_metadata).json()


df = get_data()
meta = get_meta()


st.header("Static site generators popularity  :thermometer: :star:")


"""
Static site generators (SSG) are open source tools to create blogs, 
landing pages and documentation.
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
all_langs = df.lang.unique().tolist()
langs = st.multiselect(
    "Programming languages", options=all_langs, default=all_langs, format_func=pretty
)
plot_df = df[df.lang.isin(langs)]
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
    alt.Chart(df, title="Stars vs forks")
    .mark_circle(size=60)
    .encode(
        x='stars',
        #alt.X("stars", scale=alt.Scale(type="log")),
        y='forks',
        #alt.Y("forks", scale=alt.Scale(type="log")),
        color="lang",
        tooltip=["name", "stars", "forks"],
    )
)

st.altair_chart(scatter, use_container_width=True)

"""
Consider there are two groups of SSG users: front-end engineers (FE) 
and non-specialised (NS) users doing backend work, data analysis, 
blog writing or maintaining documentation. More forks would come from FE group, 
while NS would likely to use the software as is and will not fork.

Jekyll, Octopress (end of life project), Sphinx (backbone project) 
and bookdown seem to have more forks.

There are relatively fewer forks for Hugo (maybe because it ships as 
an executable file) and eleventy (perhaps, as intended by project concept).
"""

st.header("Links")

st.write(" - ".join(f"[{name}]({url})" for name, url in zip(df.name, df.url)))

st.header("Other insights")

"""
With this dataset you can also look at following repo detail:

 - date created 
 - last commit date
 - number of open issues at repo

st.header("Data")
"""

f"""
[![](https://img.shields.io/badge/download-csv-brightgreen)]({url_csv})

Static CSV file [ssg.csv]({url_csv}) is prepared and posted via [epogrebnyak/ssg](https://github.com/epogrebnyak/ssg).

Dataset created on {meta["created"]}.

To download:

```python
import pandas as pd
url = "{url_csv}"
df = pd.read_csv(url)
```

To reproduce:

```python
from ssg import 
import pandas as pd
url = "{url_csv}"
df = pd.read_csv(url)
```


"""

st.dataframe(df)

st.header("Citation")

"""
```
Evgeniy Pogrebnyak (2021). Static site generators popularity dataset. 
URL: <https://github.com/epogrebnyak/ssg>. 
```
"""

st.header("Contacts")

"""
If you happen to have a good idea or comment about the SSG dataset, please drop 
me a line. I appreciate the feedback and look forward to hearing to SSG
use cases and this dataset applications. 

[Twitter](https://twitter.com/PogrebnyakE) is probably the easiest way 
to contact me, also my e-mail is e.pogrebnyak @ gmail dot com.
"""
