"""Popularity of static site generators (SSG) as measured by Github data."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd  # type: ignore
import yaml
from pydantic import BaseModel

from ssg.github import get_repo_state_from_handle

# Comment: may use for schema validation
allowed_languages = [
    "go",
    "js",
    "ruby",
    "python",
    "rust",
    "r",
    "swift",
    "julia",
    "haskell",
    "java",
]


class SSG(BaseModel):
    name: str
    github_handle: str  # TODO: must enforce /
    lang: str  # TODO: must enforce fix list of languages
    exec: Optional[bool] = None
    twitter: str = ""
    site: str = ""
    comment: str = ""


def read_item(key: str, values: Dict) -> SSG:
    empty_dict = {
        "name": "",
        "github_handle": "",
        "lang": "",
        "exec": None,
        "twitter": "",
        "site": "",
    }
    d = empty_dict.copy()
    d["github_handle"] = key
    d["name"] = key.split("/")[1]
    d.update(values)
    return SSG(**d)


def read_text(filename) -> str:
    return Path(filename).read_text()


def extract_yaml(text: str) -> Dict:
    return yaml.load(text, Loader=yaml.SafeLoader)


def to_ssg_list(param_dict) -> List[SSG]:
    return [read_item(k, v) for k, v in param_dict.items()]


def get_repo_state(ssg: SSG):
    return get_repo_state_from_handle(ssg.github_handle)


# TODO: can use typing check on dataframe
def make_dataframe_from_ssg(ssg_list: List[SSG]) -> pd.DataFrame:
    df = pd.DataFrame({**s.dict(), **get_repo_state(s).dict()} for s in ssg_list)
    for key in ["created", "modified"]:
        df[key] = df[key].map(lambda x: pd.to_datetime(x).date())
    return df.sort_values("stars", ascending=False).set_index("name")


def get_dataframe(yaml_filename: str) -> pd.DataFrame:
    text = read_text(yaml_filename)
    param_dict = extract_yaml(text)
    return make_dataframe_from_ssg(to_ssg_list(param_dict))


def yaml_to_csv(
    folder,
    yaml_filename="ssg.yaml",
    csv_filename="ssg.csv",
    columns=[
        "github_handle",
        "url",
        "homepage",
        "lang",
        "repo_lang",
        "created",
        "modified",
        "stars",
        "forks",
        "open_issues",
    ],
):
    csv_path = os.path.join(folder, csv_filename)
    yaml_path = os.path.join(folder, yaml_filename)
    df = get_dataframe(yaml_path)[columns]
    df.to_csv(csv_path)
    return df, csv_path


def metadata():
    return {
        "name": "Github data for static site generators popularity",
        "created": datetime.today().date().isoformat(),
        "date_columns": ["created", "modified"],
        "repo_url": "https://github.com/epogrebnyak/ssg-dataset/",
        "data_url": "https://github.com/epogrebnyak/ssg-dataset/blob/main/data/ssg.csv",
    }


def write_metadata(folder: Path, filename: str = "metadata.json") -> Path:
    path = folder / filename
    path.write_text(json.dumps(metadata()), encoding="utf-8")
    return path


def create_all(folder):
    _, p1 = yaml_to_csv(folder)
    print("Wrote", p1)
    p2 = write_metadata(folder)
    print("Wrote", p2)