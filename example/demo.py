import datetime
import tempfile
import pandas as pd
from ssg.stars import yaml_to_csv
from pathlib import Path

yaml_doc = """
rstudio/bookdown:
  lang: r
segmentio/metalsmith:
  lang: js"""
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
