from stars import get_dataframe, md_link

def make_presentation(df):
    zf = df[['stars', 'lang', 'url']]
    zf['stars'] = zf.stars.divide(1000).round(1)
    zf.index=df.apply(lambda x: md_link(x.name, x.url), result_type='expand', axis=1) 
    del zf['url']

df = get_dataframe("ssg.yaml")
print(df)

import altair as alt
df['stars'] = df.stars.divide(1000).round(1)

ch = alt.Chart(df,
               title="Static site generators popularity (26.12.2020)",               
               ).mark_bar().encode(
     x=alt.X('stars', title="\'000 stars on Github"),
     y=alt.Y('name', 
             sort=alt.EncodingSortField(field="stars", order='descending'),
             title=""),
     color=alt.Color("lang", 
                     legend=alt.Legend(title="Language"),
                     scale=alt.Scale(scheme='tableau10'))
)
ch.show()    
