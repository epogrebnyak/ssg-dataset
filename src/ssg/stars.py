"""Popularity of static site generators (SSG) as measured by Github data."""

import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, List

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


def to_dicts(yaml_dict):
    return [
        dict(
            name=name(k),
            handle=k,
            lang=v["lang"],
            exec=v.get("exec", False),  # not shown in csv
            twitter=v.get("twitter", ""),  # not shown in csv
            site=v.get("site", ""),  # not shown in csv
        )
        for k, v in yaml_dict.items()
    ]


def read_dicts(filename):
    return to_dicts(extract_yaml(read_text(filename)))


def make_dataframe(dicts) -> pd.DataFrame:
    raw_df = pd.DataFrame(dicts)
    for key in ["created", "modified"]:
        raw_df[key] = raw_df[key].map(lambda x: pd.to_datetime(x).date())
    raw_df = raw_df.sort_values("stars", ascending=False)
    raw_df.index = raw_df.name
    return raw_df


def add_github_data(dicts):
    for d in dicts:
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
    return dicts


def get_dataframe(yaml_filename: str) -> pd.DataFrame:
    text = read_text(yaml_filename)
    dicts = to_dicts(extract_yaml(text))
    dicts2 = add_github_data(dicts)
    return make_dataframe(dicts2)


def metadata():
    return {
        "name": "Github data for static site generators popularity",
        "created": datetime.today().date().isoformat(),
        "date_columns": ["created", "modified"],
        "repo_url": "https://github.com/epogrebnyak/ssg-dataset/",
        "data_url": "https://github.com/epogrebnyak/ssg-dataset/blob/main/data/ssg.csv",
    }

def write_metadata(path):
    metadata_dict = metadata()
    with open(path, "w") as f:
        json.dump(metadata_dict, f)


def yaml_to_csv(
    folder,
    yaml_filename="ssg.yaml",
    csv_filename="ssg.csv",
    meta_filename="metadata.json",
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
    def there(filename):
        return os.path.join(folder, filename)

    df = get_dataframe(there(yaml_filename))
    df[columns].to_csv(there(csv_filename))
    print("Wrote", there(csv_filename))
    write_metadata(there(meta_filename))
    print("Wrote", there(meta_filename))
    return df


if __name__ == "__main__":
    pass
