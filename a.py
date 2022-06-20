# %%
import httpx 

r = httpx.get("https://raw.githubusercontent.com/ozh/github-colors/master/colors.json").json()
r2 = {k.lower(): v["color"] for k, v in r.items()} 
# %%
from ssg.stars import allowed_languages

for lang in allowed_languages:
    print(lang, r2.get(lang))
# %%
import pandas as pd
url = ("https://raw.githubusercontent.com/"
       "epogrebnyak/ssg-dataset/main/data/ssg.csv")
df = pd.read_csv(url, parse_dates=["created", "modified"])


# %%
