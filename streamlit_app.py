import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Github stars for static site generators (SSG)",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed",
)

url = "https://raw.githubusercontent.com/epogrebnyak/ssg/main/data/ssg.csv"

st.header("Static site generators popularity  :thermometer: :star:")

"""
Static site generators are tools to create blogs, landing pages and documentation.
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


st.header("Forks")
"""
Forks are copies of orginal repo made by users to submit code additions 
to original repo or work on own version of the software. 
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
Idea: if there are two groups of SSG users - front-end engineers (FE) 
and non-specialised (NS), common users, more forks would come from FE group, 
while NS would use the software as is and will not fork.

More forks:

 - Jekyll, Octopress (all Ruby)
 - Sphinx, bookdown

Less forks:
  - Hugo (ships as binary)
  - eleventy 
"""

st.header("Discussion")

"""
[![](https://user-images.githubusercontent.com/9265326/103943179-ae5db400-5142-11eb-90be-111c8c520f93.png)][link]

[link]: https://twitter.com/PogrebnyakE/status/1343105678261555200
"""

st.subheader("Links")
st.write("\n".join(f"- [{name}]({url})" for name, url in zip(df.name, df.url)))


st.subheader("Data")
st.dataframe(df)
f"""
Static CSV file: [ssg.csv]({url}) (collected with [epogrebnyak/ssg](https://github.com/epogrebnyak/ssg)).
"""
