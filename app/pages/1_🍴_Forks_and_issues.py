import altair as alt
import streamlit as st

from data import get_data, get_github_scale

_df = get_data()
github_scale = get_github_scale()

st.header("Forks")
"""
Forks are copies of orginal repo made by other users to submit code modifications
or create own versions of software.

More forks indicate either active development of a package
or code reuse in other projects.
"""

scatter = (
    alt.Chart(_df, title="Stars vs forks")
    .mark_circle(size=60)
    .encode(
        x="stars",
        y="forks",
        color=alt.Color(
            "lang", legend=alt.Legend(title="Language"), scale=github_scale
        ),
        tooltip=["name", "stars", "forks"],
    )
)

st.altair_chart(scatter, use_container_width=True)

"""
Who are people doing the forks? Consider two groups of users:

- front-end engineers (FE), usually proficient with HTML, CSS and JavaScript, and
- non-specialised (NS) users who do other kinds of work (eg backend, data analysis
  or tasks outside software development) and need to write a blog, lay out documentation
  or simply make a small website.

More forks would come from FE group, while NS would likely use the software
as is, will not fork (and may not even star a project on Github).

Another source of forks are end-of-life projects.
Before project is retired users may do more forks to preserve the software
for future development and use.
Notable example of this kind project and extensive forks is Octopress.
"""

st.header("Open issues")

"""
More open issues in repository may be due to rapid project development or
to accumulated technical debt.
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
        color=alt.Color(
            "lang", legend=alt.Legend(title="Language"), scale=github_scale
        ),
        tooltip=["name", "stars", "forks"],
    )
)

st.altair_chart(scatter2, use_container_width=True)
st.altair_chart(scatter2, use_container_width=True)
