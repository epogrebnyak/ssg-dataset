"""Popularity of static site generators (SSG) as measured by Github data."""

import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd  # type: ignore
import requests
import requests_cache  # type: ignore
import yaml
from dotenv import load_dotenv
from pydantic import BaseModel

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


class SSG(BaseModel):
    name: str
    github_handle: str  # must enforce /
    lang: str  # must enforce fix list of languages
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


def date_only(s):
    return s[: 4 + 2 + 2 + 2]


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


def read_text(filename) -> str:
    return Path(filename).read_text()


def extract_yaml(text: str):
    return yaml.load(text, Loader=yaml.SafeLoader)


def to_ssg(yaml_dict) -> List[SSG]:
    return [read_item(k, v) for k, v in yaml_dict.items()]


def add_github_data(s: SSG) -> Dict:
    handle = s.github_handle
    d = s.dict()
    d["url"] = url(handle)
    d["modified"] = date_only(last_modified(handle))
    r = Repo(handle)
    print("Retrieved data for", handle)
    d["stars"] = r.n_stars()
    d["forks"] = r.n_forks()
    d["open_issues"] = r.open_issues()
    d["created"] = date_only(r.created_at())
    d["homepage"] = r.homepage()
    d["repo_lang"] = r.language()
    return d


class RepoState(BaseModel):
    repo_lang: str
    url: str
    homepage: str
    created: str  # change to date
    modified: str  # change to date
    stars: int
    forks: int
    open_issues: int


def get_repo_state(handle):
    print("Retrieving data for", handle, "...")
    repo = get_repo(handle)
    return RepoState(
        repo_lang=repo["language"],
        url=url(handle),
        homepage=repo["homepage"],
        created=date_only(repo["created_at"]),
        modified=date_only(last_modified(handle)),
        stars=repo["stargazers_count"],
        forks=repo["forks_count"],
        open_issues=repo["open_issues_count"],
    )


def stream_dicts(param_dict: dict) -> List[Dict]:
    return [add_github_data(d) for d in to_ssg(param_dict)]


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
        "github_handle",
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
