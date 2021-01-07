import altair as alt

from stars import get_dataframe

df = get_dataframe("data/ssg.yaml")
df["stars"] = df.stars.divide(1000).round(1)
print(df)


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
            scale=alt.Scale(scheme="tableau10"),
        ),
    )
)

# will need "conda install -c conda-forge altair_saver"
chart.save('images/plot.png')
