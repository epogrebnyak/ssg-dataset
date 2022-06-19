"""Popularity of static site generators (SSG) as measured by Github data."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd  # type: ignore
import requests
import requests_cache  # type: ignore
import yaml
from dotenv import load_dotenv
from pydantic import BaseModel

# TODO: sepaare code for generec queries about github and SSGs into two modules  

# Comment: need stable location for the file - may appear in different folders for example and tests
requests_cache.install_cache("cache_1")

load_dotenv(".config.env")
USER = os.getenv("USER", "")
TOKEN = os.getenv("TOKEN", "")

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


def get_repo(handle: str) -> Dict:
    return fetch(make_api_url(handle))


def get_commits(handle: str) -> List[Any]:
    return fetch(make_api_url_commits(handle))


def fetch(url: str, username:str=USER, token:str=TOKEN):
    if TOKEN:
        r = requests.get(url, auth=(username, token))
    else:
        r = requests.get(url)
    return r.json()


def last_modified(handle: str) -> str:
    _last = get_commits(handle)[0]
    return _last["commit"]["author"]["date"]


def date_only(s):
    return s[: 4 + 2 + 2 + 2] # TODO: change to date


def read_text(filename) -> str:
    return Path(filename).read_text()


def extract_yaml(text: str) -> Dict:
    return yaml.load(text, Loader=yaml.SafeLoader)


def to_ssg_list(yaml_dict) -> List[SSG]:
    return [read_item(k, v) for k, v in yaml_dict.items()]


class RepoState(BaseModel):
    repo_lang: str
    url: str
    homepage: str
    created: str  # TODO: change to date
    modified: str  # TODO: change to date
    stars: int
    forks: int
    open_issues: int


def get_repo_state_from_handle(handle: str) -> RepoState:
    print("Retrieving data for", handle, "...")
    repo = get_repo(handle)
    return RepoState(
        repo_lang=repo["language"],
        url=url(handle),
        homepage=repo["homepage"],
        created=date_only(repo["created_at"]),
        modified=date_only(last_modified(handle)),
        stars=int(repo["stargazers_count"]),
        forks=int(repo["forks_count"]),
        open_issues=int(repo["open_issues_count"]),
    )


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


def write_metadata(folder: Path, filename: str = "metadata.json") -> Path:
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
