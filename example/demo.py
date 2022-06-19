import datetime
import tempfile
import pandas as pd
from ssg.stars import yaml_to_csv, extract_yaml, stream_dicts
from pathlib import Path
from pydantic import BaseModel
from typing import Optional, Dict


class SSG(BaseModel):
    name: str
    github_handle: str  # must enforce /
    lang: str  # must enforce fix list of languages
    exec: Optional[bool] = None
    twitter: str = ""
    site: str = ""


s = SSG(
    name="bookdown", github_handle="rstudio/bookdown", lang="r", site="bookdown.org"
)

empty_dict = {
    "name": "",
    "github_handle": "",
    "lang": "",
    "exec": None,
    "twitter": "",
    "site": "",
}
d = empty_dict.copy()


def read_item(key: str, values: Dict) -> SSG:
    d = empty_dict.copy()
    d["github_handle"] = key
    d["name"] = key.split("/")[1]
    d.update(values)
    return SSG(**d)


s2 = read_item("rstudio/bookdown", {"lang": "r", "site": "bookdown.org"})
assert s == s2

yaml_doc = """
rstudio/bookdown:
  lang: r
segmentio/metalsmith:
  lang: js"""

yaml_raw_dict = {
    "rstudio/bookdown": {"lang": "r"},
    "segmentio/metalsmith": {"lang": "js"},
}

raw_dict = extract_yaml(yaml_doc)
assert raw_dict == yaml_raw_dict

af = stream_dicts(yaml_raw_dict)
assert af == [
    {
        "name": "bookdown",
        "github_handle": "rstudio/bookdown",
        "lang": "r",
        "exec": None,
        "twitter": "",
        "site": "",
        "url": "https://github.com/rstudio/bookdown/",
        "modified": "2022-06-14",
        "stars": 2985,
        "forks": 1135,
        "open_issues": 175,
        "created": "2015-10-28",
        "homepage": "https://pkgs.rstudio.com/bookdown/",
        "repo_lang": "JavaScript",
    },
    {
        "name": "metalsmith",
        "github_handle": "segmentio/metalsmith",
        "lang": "js",
        "exec": None,
        "twitter": "",
        "site": "",
        "url": "https://github.com/segmentio/metalsmith/",
        "modified": "2022-06-10",
        "stars": 7736,
        "forks": 667,
        "open_issues": 32,
        "created": "2014-02-04",
        "homepage": "https://metalsmith.io",
        "repo_lang": "JavaScript",
    },
]

with tempfile.TemporaryDirectory() as tmpdir:
    yaml_path = Path(tmpdir) / "ssg.yaml"
    csv_path = Path(tmpdir) / "ssg.csv"
    columns = [
        "github_handle",
        "created",
        "modified",
        "stars",
        "forks",
        "open_issues",
        "lang",
        "repo_lang",
        "url",
    ]
    yaml_path.write_text(yaml_doc, encoding="utf-8")
    df = yaml_to_csv(tmpdir, "ssg.yaml", "ssg.csv", columns)
    df2 = pd.read_csv(csv_path, parse_dates=["created", "modified"])
