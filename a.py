# %%
import requests 
from ssg.stars import allowed_languages, pretty


def palette(allowed_languages):
    r = requests.get("https://raw.githubusercontent.com/ozh/github-colors/master/colors.json").json()
    return {pretty(lang):r[pretty(lang)]["color"] for lang in allowed_languages}
# %%
import pandas as pd
url = ("https://raw.githubusercontent.com/"
       "epogrebnyak/ssg-dataset/main/data/ssg.csv")
df = pd.read_csv(url, parse_dates=["created", "modified"])


# %%
