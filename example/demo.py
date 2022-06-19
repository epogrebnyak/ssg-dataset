import datetime
import tempfile
import pandas as pd
from ssg.stars import yaml_to_csv, extract_yaml, from_raw_dict
from pathlib import Path

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

af = from_raw_dict(yaml_raw_dict)
assert af == [
    {
        "name": "bookdown",
        "handle": "rstudio/bookdown",
        "lang": "r",
        "exec": False,
        "twitter": "",
        "site": "",
        "url": "https://github.com/rstudio/bookdown/",
        "modified": "2022-06-14T14:45:52Z",
        "stars": 2985,
        "forks": 1135,
        "open_issues": 175,
        "created": "2015-10-28T05:03:18Z",
        "homepage": "https://pkgs.rstudio.com/bookdown/",
        "repo_lang": "JavaScript",
    },
    {
        "name": "metalsmith",
        "handle": "segmentio/metalsmith",
        "lang": "js",
        "exec": False,
        "twitter": "",
        "site": "",
        "url": "https://github.com/segmentio/metalsmith/",
        "modified": "2022-06-10T16:11:07Z",
        "stars": 7736,
        "forks": 667,
        "open_issues": 32,
        "created": "2014-02-04T03:46:22Z",
        "homepage": "https://metalsmith.io",
        "repo_lang": "JavaScript",
    },
]

with tempfile.TemporaryDirectory() as tmpdir:
    yaml_path = Path(tmpdir) / "ssg.yaml"
    csv_path = Path(tmpdir) / "ssg.csv"
    columns = [
        "handle",
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
