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

url = "https://raw.githubusercontent.com/epogrebnyak/ssg/main/data/ssg.csv"

st.header("Static site generators popularity  :thermometer: :star:")


"""
Static site generators (SSG) are tools to create blogs, landing pages and documentation.
"""

st.header("Github data")

st.subheader("1. Stars")
"""
Number of stars in a Github repository is a proxy for SSG popularity, at least among developers.
Surely a lot of people can use a SSG without ever looking at the Github repo, but the stars 
count cannot be ignored.
"""


def pretty(s: str) -> str:
    try:
        return dict(js="JavaScript")[s]
    except KeyError:
        return s.capitalize()


@st.cache
def get_data():
    df = pd.read_csv(url)
    df["lang"] = df.lang.map(pretty)
    return df

@st.cache
def date_created():
    return requests.get("https://raw.githubusercontent.com/epogrebnyak/ssg/main/data/metadata.json").json()


df = get_data()


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


st.subheader("2. Forks")
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
and non-specialised (NS) users doing backend work, data analysis or 
blog writing. More forks would come from FE group, while NS 
would likely to use the software as is and will not fork.

Jekyll, Octopress (end of life project), Sphinx (backbone project) 
and bookdown seem to have more forks.

There are relatively less forks for Hugo (maybe because it ships as 
an executable file) and eleventy (perhaps, the intent to offer it "as is"
to users).
"""

st.subheader("Links")

st.write(" - ".join(f"[{name}]({url})" for name, url in zip(df.name, df.url)))



st.header("Discussion")

"""
Users:

 - people from different backgrounds adopt different tools
 - front-end (FE) engineers would also care less about main theme for SSG, but would fork
 - non-frontend people are a big user group, ready-made themes are important for them, they don't fork

Theme popularity:

- top Hugo themes  even+learn+coder+academic each have 1-1.1k github stars, while @GoHugoIO
  itself is 49k stars
- Jekyll (41k) -> Mimimal Mistakes (7k) 
- mkdocs (11k) ->  mkdocs-material by @squidfunk (5.2k)
- themes not transferable between SSGs due to semantics

Total universe:

- Next.js and Wordpress popular for site-building, but htey are server-side, not exactly SSG
- many CMS

Twitter threads:

- [Dec 27, 2020](https://twitter.com/PogrebnyakE/status/1343105678261555200)
- [Jan 8, 2021](https://twitter.com/PogrebnyakE/status/1347508424674783234)

Facebook:

- [Jan 8, 2021](https://www.facebook.com/e.pogrebnyak/posts/10218455975936127)

Open questions:

1. Do 'created' vs 'modified' repo dates ring any bell? (Hint: depreciations, project life, stars/day rate)
2. Imagine you knew the total user base per programming language, how would you use it?
3. Imagine you had a theme list per SSG, what would you do?

"""

st.header("Data")
st.dataframe(df)

"""
[![](https://img.shields.io/badge/download-csv-brightgreen)](https://raw.githubusercontent.com/epogrebnyak/ssg/main/data/ssg.csv)
"""

f"""
Static CSV file [ssg.csv]({url}) is prepared by [epogrebnyak/ssg](https://github.com/epogrebnyak/ssg).
"""


f"""
Dataset created on {date_created()}.
"""

"""
To download:

```python
import pandas as pd
url = "https://raw.githubusercontent.com/epogrebnyak/ssg/main/data/ssg.csv"
df = pd.read_csv(url)
```
"""

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
use cases, dataset applications and other. [Twitter](https://twitter.com/PogrebnyakE)
 is probably the easiest way to contact me.
"""

