"""Popularity of static site generators (SSG) as measured by Github data."""

import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, List
from typing import Dict, List


import pandas as pd  # type: ignore
import requests
import requests_cache  # type: ignore
import yaml
from dotenv import load_dotenv

# Comment: need stable location for the file - may appear in different folders for example and tests
requests_cache.install_cache("cache_1")

load_dotenv(".config.env")
USER = os.getenv("USER")
TOKEN = os.getenv("TOKEN")

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


def url(handle):
    return f"https://github.com/{handle}/"


def make_api_url(
    handle: str,
) -> str:
    return f"https://api.github.com/repos/{handle}"


def make_api_url_commits(
    handle: str,
) -> str:
    return f"https://api.github.com/repos/{handle}/commits"


def get_repo(handle: str) -> str:
    return fetch(make_api_url(handle))


def get_commits(handle: str) -> List[Any]:
    return fetch(make_api_url_commits(handle))


def fetch(url: str, username=USER, token=TOKEN):
    if TOKEN:
        r = requests.get(url, auth=(username, token))
    else:
        r = requests.get(url)
    return r.json()


def last_modified(handle: str) -> str:
    _last = get_commits(handle)[0]
    return _last["commit"]["author"]["date"]


class Repo:
    def __init__(self, handle: str):
        self.handle = handle
        self.repo = get_repo(handle)

    def n_stars(self):
        return self.repo["stargazers_count"]

    def n_forks(self):
        return self.repo["forks_count"]

    def open_issues(self):
        return self.repo["open_issues_count"]

    def created_at(self):
        return self.repo["created_at"]

    def homepage(self):
        return self.repo["homepage"]

    def language(self):
        return self.repo["language"]


def name(handle: str):
    return handle.split("/")[1]


def read_text(filename) -> str:
    return Path(filename).read_text()


def extract_yaml(text: str):
    return yaml.load(text, Loader=yaml.SafeLoader)


# will change with Pydantic
def norm(key, values):
    return dict(
        name=name(key),
        handle=key,
        lang=values["lang"],
        exec=values.get("exec", False),  # not shown in csv
        twitter=values.get("twitter", ""),  # not shown in csv
        site=values.get("site", ""),  # not shown in csv
    )


def to_dicts(yaml_dict):
    return [norm(k, v) for k, v in yaml_dict.items()]


def add_github_data(d: dict):
    handle = d["handle"]
    d["url"] = url(handle)
    d["modified"] = last_modified(handle)
    r = Repo(handle)
    d["stars"] = r.n_stars()
    d["forks"] = r.n_forks()
    d["open_issues"] = r.open_issues()
    d["created"] = r.created_at()
    d["homepage"] = r.homepage()
    d["repo_lang"] = r.language()
    print("Retrieved data for", handle)
    return d


def stream_dicts(param_dict: dict) -> List[Dict]:
    return [add_github_data(d) for d in to_dicts(param_dict)]


def make_dataframe(dicts: List[Dict]) -> pd.DataFrame:
    raw_df = pd.DataFrame(dicts)
    for key in ["created", "modified"]:
        raw_df[key] = raw_df[key].map(lambda x: pd.to_datetime(x).date())
    raw_df = raw_df.sort_values("stars", ascending=False)
    raw_df.index = raw_df.name
    return raw_df


def get_dataframe(yaml_filename: str) -> pd.DataFrame:
    text = read_text(yaml_filename)
    param_dict = extract_yaml(text)
    return make_dataframe(stream_dicts(param_dict))


def yaml_to_csv(
    folder,
    yaml_filename="ssg.yaml",
    csv_filename="ssg.csv",
    columns=[
        "handle",
        "created",
        "modified",
        "stars",
        "forks",
        "open_issues",
        "lang",
        "repo_lang",
        "url",
    ],
):
    csv_path = os.path.join(folder, csv_filename)
    yaml_path = os.path.join(folder, yaml_filename)
    df = get_dataframe(yaml_path)
    df[columns].to_csv(csv_path)
    return df, csv_path


def metadata():
    return {
        "name": "Github data for static site generators popularity",
        "created": datetime.today().date().isoformat(),
        "date_columns": ["created", "modified"],
        "repo_url": "https://github.com/epogrebnyak/ssg-dataset/",
        "data_url": "https://github.com/epogrebnyak/ssg-dataset/blob/main/data/ssg.csv",
    }


def write_metadata(folder: Path, filename: str = "metadata.json") -> None:
    path = folder / filename
    path.write_text(json.dumps(metadata()), encoding="utf-8")
    return path


def create_all(folder):
    _, p1 = yaml_to_csv(folder)
    print("Wrote", p1)
    p2 = write_metadata(folder)
    print("Wrote", p2)


if __name__ == "__main__":
    pass
