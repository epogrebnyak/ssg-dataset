"""Popularity of static site generators (SSG).

Creates a dataset in a CSV file based on listing of SSG Github addresses (handles) in YAML file.

Example:

  yaml_to_csv_by_file("data/ssg.yaml", "data/ssg.csv")
  create_all("data")

"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union

import pandas as pd  # type: ignore
import yaml
from pydantic import BaseModel

from ssg.github import get_repo_state_from_handle

__all__ = ["yaml_to_csv_by_file", "create_all"]

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
    "elm",
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


def read_text(filename) -> Optional[str]:
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


def get_dataframe(yaml_filename: Union[Path, str]) -> pd.DataFrame:
    text = read_text(yaml_filename)
    param_dict = extract_yaml(text)
    return make_dataframe_from_ssg(to_ssg_list(param_dict))


def yaml_to_csv_by_file(
    yaml_path: Union[Path, str],
    csv_path: Union[Path, str],
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
    df = get_dataframe(yaml_path)[columns]
    df.to_csv(csv_path)
    return df


def metadata():
    return {
        "name": "Github data for static site generators popularity",
        "created": datetime.today().date().isoformat(),
        "date_columns": ["created", "modified"],
        "repo_url": "https://github.com/epogrebnyak/ssg-dataset/",
        "data_url": "https://github.com/epogrebnyak/ssg-dataset/blob/main/data/ssg.csv",
    }


def write_metadata(folder: Union[Path, str], filename: str = "metadata.json") -> Path:
    path = Path(folder) / filename
    path.write_text(json.dumps(metadata()), encoding="utf-8")
    return path


def create_all(folder: Union[Path, str]) -> None:
    yaml_path = Path(folder) / "ssg.yaml"
    csv_path = Path(folder) / "ssg.csv"
    yaml_to_csv_by_file(yaml_path, csv_path)
    print("Wrote", csv_path)
    metadata_path = write_metadata(folder)
    print("Wrote", metadata_path)
