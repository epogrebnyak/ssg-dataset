[![Download CSV](https://img.shields.io/badge/download-csv-brightgreen)]({url_csv})
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/epogrebnyak/ssg-dataset/main)
[![Demo in Google Colab](https://img.shields.io/badge/Colab-open-orange)][colab]

[colab]: https://colab.research.google.com/drive/1041e6yOyVRty5lirnbZOAU1zJ3TN77ta

# Popularity of static site generators

Static site generators are tools to create blogs, landing pages and documentation.

This repo contains Github data (stars, forks, issues, create and last modified dates) for 30 open source static site generators (SSG). The repo also contains the code used to create the dataset. 


## Try live

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)][st]
[![Demo in Google Colab](https://img.shields.io/badge/colab-open-orange)][colab]

[st]: https://share.streamlit.io/epogrebnyak/ssg-dataset/main


[Streamlit app][st] lays out a data story about SSGs with several visualisations. 
[Colab][colab] is a try and see playground with some code for chart.

## Dataset

The stable URL for dataset is:

```
https://raw.githubusercontent.com/epogrebnyak/ssg-dataset/main/data/ssg.csv
```

To download:

```python
import pandas as pd
url = ("https://raw.githubusercontent.com/"
       "epogrebnyak/ssg-dataset/main/data/ssg.csv")
df = pd.read_csv(url, parse_dates=["created", "modified"])
```

Sample:

|                                                                  |   '000 stars | Language   |
|------------------------------------------------------------------|--------------|------------|
| [hugo](https://github.com/gohugoio/hugo/)                        |         49.3 | go         |
| [gatsby](https://github.com/gatsbyjs/gatsby/)                    |         48.6 | js         |
| [jekyll](https://github.com/jekyll/jekyll/)                      |         42.0 | ruby       |
| [hexo](https://github.com/hexojs/hexo/)                          |         32.0 | js         |
| [vuepress](https://github.com/vuejs/vuepress/)                   |         18.2 | js         |
| [mkdocs](https://github.com/mkdocs/mkdocs/)                      |         11.3 | python     |
| [pelican](https://github.com/getpelican/pelican/)                |         10.1 | python     |
| [octopress](https://github.com/imathis/octopress/)               |          9.4 | ruby       |
| [eleventy](https://github.com/11ty/eleventy/)                    |          8.2 | js         |
| [metalsmith](https://github.com/segmentio/metalsmith/)           |          7.6 | js         |
| [gridea](https://github.com/getgridea/gridea/)                   |          6.8 | js         |
| [middleman](https://github.com/middleman/middleman/)             |          6.7 | ruby       |
| [mdBook](https://github.com/rust-lang/mdBook/)                   |          5.6 | rust       |
| [zola](https://github.com/getzola/zola/)                         |          4.8 | rust       |
| [sphinx](https://github.com/sphinx-doc/sphinx/)                  |          3.7 | python     |
| [wintersmith](https://github.com/jnordberg/wintersmith/)         |          3.5 | js         |
| [lektor](https://github.com/lektor/lektor/)                      |          3.4 | python     |
| [Cactus](https://github.com/eudicots/Cactus/)                    |          3.4 | python     |
| [Publish](https://github.com/JohnSundell/Publish/)               |          3.1 | swift      |
| [bookdown](https://github.com/rstudio/bookdown/)                 |          2.3 | r          |
| [hakyll](https://github.com/jaspervdj/hakyll/)                   |          2.3 | haskell    |
| [nikola](https://github.com/getnikola/nikola/)                   |          2.1 | python     |
| [fastpages](https://github.com/fastai/fastpages/)                |          2.1 | python     |
| [jupyter-book](https://github.com/executablebooks/jupyter-book/) |          2.0 | python     |
| [scully](https://github.com/scullyio/scully/)                    |          2.0 | js         |
| [nanoc](https://github.com/nanoc/nanoc/)                         |          1.9 | ruby       |
| [ihp](https://github.com/digitallyinduced/ihp/)                  |          1.7 | haskell    |
| [cobalt.rs](https://github.com/cobalt-org/cobalt.rs/)            |          0.9 | rust       |
| [Franklin.jl](https://github.com/tlienart/Franklin.jl/)          |          0.4 | julia      |
| [bridgetown](https://github.com/bridgetownrb/bridgetown/)        |          0.3 | ruby       |