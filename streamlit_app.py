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

@st.cache
def get_data():
    return pd.read_csv(url)


df = get_data()
df["stars"] = df.stars.divide(1000).round(1)

chart = (
    alt.Chart(
        df,
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

st.subheader("Data")

f"""
Data collected with [epogrebnyak/ssg](https://github.com/epogrebnyak/ssg). Static CSV file: [ssg.csv]({url})


"""

st.dataframe(df)
