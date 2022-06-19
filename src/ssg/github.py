"""Get Github repo statistics."""

import os
from typing import Any, Dict, List, Optional

import pandas as pd  # type: ignore
import requests
import requests_cache  # type: ignore
from dotenv import load_dotenv
from pydantic import BaseModel

__all__ = ["get_repo_state_from_handle"]


# Comment: need stable location for the file - may appear in different folders for example and tests
requests_cache.install_cache("cache_1")

load_dotenv(".config.env")
USER = os.getenv("USER", "")
TOKEN = os.getenv("TOKEN", "")


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


def fetch(url: str, username: str = USER, token: str = TOKEN):
    if TOKEN:
        r = requests.get(url, auth=(username, token))
    else:
        r = requests.get(url)
    return r.json()


def last_modified(handle: str) -> str:
    _last = get_commits(handle)[0]
    return _last["commit"]["author"]["date"]


def date_only(s):
    return s[: 4 + 2 + 2 + 2]  # TODO: change to date


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
    """Return Github repo statistics by repo handle.

    Example:

       get_repo_state_from_handle("withastro/astro")

    returns

    ```
    RepoState(
        repo_lang="TypeScript",
        url="https://github.com/withastro/astro/",
        homepage="https://astro.build",
        created="2021-03-15",
        modified="2022-06-19",
        stars=12422,
        forks=641,
        open_issues=98,
    )
    ```
    """
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
