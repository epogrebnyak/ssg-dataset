[![pytest](https://github.com/epogrebnyak/ssg-dataset/workflows/pytest/badge.svg)](https://github.com/epogrebnyak/ssg-dataset/actions)
![count](app/ssg_count.svg)

# Popularity of static site generators

Static site generators are tools to create documentation, blogs and landing pages.

This repo contains Github data (stars, forks, issues, create and last modified dates) for 40+ popular open source static site generators (SSG) and code to create the dataset.

## Try live on Streamlit

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)][st]

[Streamlit app][st] lays out a data story about SSGs with several visualisations.

[![Streamlit Screenshot](https://user-images.githubusercontent.com/9265326/174656606-24102187-411c-462d-adb7-b8bb1a1a6db0.png)][st]


### Google Colab

[![Demo in Google Colab](https://img.shields.io/badge/Colab-Open-orange)][colab]

[Colab][colab] is a try-and-see playground with some code for charts.

[colab]: https://colab.research.google.com/drive/1Mp_6Ktk-t-a1fQzggvRJauwFLXaWzjAL#scrollTo=xMZoFSeCT1m2
[st]: ssg-dataset.streamlit.app/

## Dataset

[![Download CSV](https://img.shields.io/badge/download-CSV-brightgreen)][url]
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4429834.svg)](https://doi.org/10.5281/zenodo.4429834)

[url]: https://raw.githubusercontent.com/epogrebnyak/ssg-dataset/main/data/ssg.csv

The stable URL for dataset is <https://raw.githubusercontent.com/epogrebnyak/ssg-dataset/main/data/ssg.csv>

To download:

```python
import pandas as pd
url = ("https://raw.githubusercontent.com/"
       "epogrebnyak/ssg-dataset/main/data/ssg.csv")
df = pd.read_csv(url, parse_dates=["created", "modified"])
```

## How to update dataset

### Get a Github token

You will need a Github token to retrieve stats for many repos. Write out `.config.env`
near to where you run your Python code:

```toml
GH_USER="your Github username here"
GH_TOKEN="your Github personal token here"
```

Your Github personal token is [here](https://github.com/settings/tokens/) and
token documentation is [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

### Update CSV file

Use `ssg.yaml_to_csv()` to update CSV file:

```python
from ssg import yaml_to_csv

yaml_to_csv("data/ssg.yaml", "data/ssg.csv")
```

[update]: https://github.com/epogrebnyak/ssg-dataset/blob/main/example/update.py

You can also run [`example/update.py`][update] to update `data/ssg.csv`:

```
poetry run python example/update.py
```

## More links about SSG

### Performance

[Static Site Generators Build Performance Testing](https://ssg-build-performance-tests.netlify.app/):

- framework-based SSG: gatsby, next, nuxt
- non-framework-based SSG: astro, eleventy, hugo, jekyll

### Listings

- [347 Generators listed at Jamstack Site Generators](https://jamstack.org/generators/)
- [The definitive listing of Static Site Generators — all 460 of them!](https://staticsitegenerators.net/)
- [Awesome Static Web Site Generators](https://github.com/myles/awesome-static-generators)

### Samples

- [Stay Static </> One Design, Many Samples](http://staystatic.github.io/)

### Hosting services

- [Gitlab](https://gitlab.com/pages?_gl=1%2a1wldy0n%2a_ga%2aMTQ2Mzg2NjA0My4xNjc0OTEyMzgw%2a_ga_ENFH3X7M5Y%2aMTY3NDkxMjM4MC4xLjEuMTY3NDkxMjQ1Ni4wLjAuMA..)
- [Netlify CMS](https://www.netlifycms.org/docs/add-to-your-site/)

### Archive articles

- <https://snipcart.com/blog/choose-best-static-site-generator>
- [Why Static Site Generators Are The Next Big Thing (2015)](https://www.smashingmagazine.com/2015/11/modern-static-website-generators-next-big-thing/)
- [Static Site Generator Trends (2020)](https://redmonk.com/rstephens/2020/05/18/static-site-generators/)

## Citation

Evgeny Pogrebnyak. (2021). Github data for static site generators (SSG) popularity (Version 0.1.2) [Data set]. Zenodo. http://doi.org/10.5281/zenodo.4429834
