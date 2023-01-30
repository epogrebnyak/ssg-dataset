import streamlit as st

from data import get_data, get_github_scale, url_csv

_df = get_data()
github_scale = get_github_scale()

n = len(_df)
created = str(_df.modified.max().date())
st.header("Links")

alpha = _df.sort_values("name", key=lambda s: s.str.lower())
st.write(" - ".join(f"[{name}]({url})" for name, url in zip(alpha.name, alpha.url)))

st.header("Data")

f"""
[![](https://img.shields.io/badge/download-csv-brightgreen)]({url_csv})

Static CSV file [ssg.csv]({url_csv}) is prepared and posted via [epogrebnyak/ssg](https://github.com/epogrebnyak/ssg).

Dataset created on {created}. A total of {n} SSGs listed.

To download:

```python
import pandas as pd
url = "{url_csv}"
df = pd.read_csv(url, parse_dates=["created", "modified"])
```
"""

st.dataframe(_df)
