
import streamlit as st
import altair as alt
import pandas as pd 

_df = st.session_state['df']
meta = st.session_state['meta']
github_scale = st.session_state['github_scale']
url_csv = st.session_state['url_csv']
st.header("Links")

alpha = _df.sort_values("name", key=lambda s: s.str.lower())
st.write(" - ".join(f"[{name}]({url})" for name, url in zip(alpha.name, alpha.url)))

st.header("Data")

f"""
[![](https://img.shields.io/badge/download-csv-brightgreen)]({url_csv})

Static CSV file [ssg.csv]({url_csv}) is prepared and posted via [epogrebnyak/ssg](https://github.com/epogrebnyak/ssg).

Dataset created on {meta["created"]}. A total of 
{len(_df)} SSGs listed. 

To download:

```python
import pandas as pd
url = "{url_csv}"
df = pd.read_csv(url, parse_dates=["created", "modified"])
```
"""

st.dataframe(_df)

"""
(C) Evgeny Pogrebnyak, 2021-2023
"""

