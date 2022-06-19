[![pytest](https://github.com/epogrebnyak/ssg-dataset/workflows/pytest/badge.svg)](https://github.com/epogrebnyak/ssg-dataset/actions)

# Popularity of static site generators

Static site generators are tools to create blogs, landing pages and documentation.

This repo contains Github data (stars, forks, issues, create and last modified dates) for 30+ open source static site generators (SSG) and code to create the dataset.

## Try live

### Streamlit

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)][st]

[Streamlit app][st] lays out a data story about SSGs with several visualisations.

[![Streamlit Photos](https://user-images.githubusercontent.com/9265326/174499755-4f0be21b-3488-4a2d-ba19-66336ae80436.png)][st]

### Google Colab

[![Demo in Google Colab](https://img.shields.io/badge/Colab-Open-orange)][colab]

[Colab][colab] is a try-and-see playground with some code for charts.

[st]: https://share.streamlit.io/epogrebnyak/ssg-dataset/main
[colab]: https://colab.research.google.com/drive/1041e6yOyVRty5lirnbZOAU1zJ3TN77ta

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

You will need a Github token to retreive stats for many repos. Write out `.config.env`
near to where you run your Python code:

```toml
GH_USER="your Github username here"
GH_TOKEN="your Github personal token here"
```

Your Github personal token is [here](https://github.com/settings/tokens/) and
token documentation is [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

### Update CSV file

[update]: https://github.com/epogrebnyak/ssg-dataset/blob/main/example/update.py

[`example/update.py`][update] should update `data/ssg.csv`:

```
poetry run python example/update.py
```

## More links about SSGs

### Listings

- [Awesome Static Web Site Generators](https://github.com/myles/awesome-static-generators)
- [The definitive listing of Static Site Generators — all 460 of them!](https://staticsitegenerators.net/)
- <https://jamstack.org/generators/>
- <https://www.netlifycms.org/docs/add-to-your-site/>
- [Stay Static </> One Design, Many Samples](http://staystatic.github.io/)

### Articles

- [Why Static Site Generators Are The Next Big Thing (2015)](https://www.smashingmagazine.com/2015/11/modern-static-website-generators-next-big-thing/)
- [Static Site Generator Trends (2020)](https://redmonk.com/rstephens/2020/05/18/static-site-generators/)

## Citation

Evgeny Pogrebnyak. (2021). Github data for static site generators (SSG) popularity (Version 0.1.2) [Data set]. Zenodo. http://doi.org/10.5281/zenodo.4429834

Current version is Version 0.2.2 (June 2022).
