import datetime
import tempfile
from pathlib import Path
from typing import Dict, Optional

import pandas as pd

from ssg.github import get_repo_state_from_handle
from ssg.stars import (extract_yaml, make_dataframe_from_ssg, to_ssg_list,
                       yaml_to_csv)

rs = get_repo_state_from_handle("tighten/jigsaw")

yaml_doc = """
rstudio/bookdown:
  lang: r
segmentio/metalsmith:
  lang: js"""

param_dict = extract_yaml(yaml_doc)
xs = make_dataframe_from_ssg(to_ssg_list(param_dict))


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
