import datetime
import tempfile
import pandas as pd
from ssg.stars import (
    yaml_to_csv,
    extract_yaml,
    stream_dicts,
    SSG,
    read_item,
    get_repo_state,
)
from pathlib import Path
from pydantic import BaseModel
from typing import Optional, Dict


s = SSG(
    name="bookdown", github_handle="rstudio/bookdown", lang="r", site="bookdown.org"
)

s2 = read_item("rstudio/bookdown", {"lang": "r", "site": "bookdown.org"})
assert s == s2


rs = get_repo_state("rstudio/bookdown")

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
