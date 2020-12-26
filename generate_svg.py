import altair as alt

# import plotly.graph_objects as go

# fig = go.Figure(go.Bar(
#             x=[20, 14, 23],
#             y=['giraffes', 'orangutans', 'monkeys'],
#             orientation='h'))

# fig.show()

import pandas as pd
src = pd.DataFrame({'name': {'hugo': 'hugo',
  'gatsby': 'gatsby',
  'jekyll': 'jekyll',
  'hexo': 'hexo',
  'vuepress': 'vuepress',
  'mkdocs': 'mkdocs',
  'pelican': 'pelican',
  'eleventy': 'eleventy',
  'mdBook': 'mdBook',
  'zola': 'zola',
  'sphinx': 'sphinx',
  'nikola': 'nikola',
  'jupyter-book': 'jupyter-book'},
 'stars': {'hugo': 49001,
  'gatsby': 48350,
  'jekyll': 41846,
  'hexo': 31898,
  'vuepress': 18066,
  'mkdocs': 11276,
  'pelican': 10099,
  'eleventy': 8060,
  'mdBook': 5519,
  'zola': 4679,
  'sphinx': 3690,
  'nikola': 2057,
  'jupyter-book': 1985},
 'lang': {'hugo': 'go',
  'gatsby': 'js',
  'jekyll': 'ruby',
  'hexo': 'js',
  'vuepress': 'js',
  'mkdocs': 'python',
  'pelican': 'python',
  'eleventy': 'js',
  'mdBook': 'rust',
  'zola': 'rust',
  'sphinx': 'python',
  'nikola': 'python',
  'jupyter-book': 'python'}})
src = src.sort_values("stars", ascending=False)
src['ix'] = list(reversed(range(len(src))))
src['stars'] = src.stars.divide(1000).round(1)

ch = alt.Chart(src).mark_bar().encode(
     x='stars',
     y=alt.Y('name', sort=alt.EncodingSortField(field="stars", order='descending')),
     color="lang"
)

ch.show()