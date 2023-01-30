import altair as alt
import pandas as pd
import streamlit as st

_df = st.session_state["df"]
meta = st.session_state["meta"]
github_scale = st.session_state["github_scale"]

st.header("Project lifetime")

"""
The longest-running static site generators are based on Ruby.

The youngest SSG are bridgetown (again Ruby), vitepress, nuxt-content, 
nextra and astro (JavaScript). 
"""


def lapsed(x, today=meta["created"]):
    t = pd.to_datetime(today)
    return (t - x).days


def year_fractional(dt):
    frac = (dt - pd.Timestamp(year=dt.year, month=1, day=1)).days / 365
    return dt.year + frac


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
            scale=github_scale,
        ),
        tooltip=["name", "stars", "years"],
    )
)
st.altair_chart(ch, use_container_width=True)

"""
Several SSG are no longer maintained - one in Ruby, Python, JavaScript, Swift and elm.
"""
ch = (
    alt.Chart(
        t.sort_values("modified", ascending=True).head(10),
        title="Out of business or stable?",
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
            scale=github_scale,
        ),
        tooltip=["name", "stars", "years", "silent"],
    )
)
st.altair_chart(ch, use_container_width=True)
