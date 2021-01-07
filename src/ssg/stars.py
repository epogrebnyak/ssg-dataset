"""Popularity statistics for static site generators (SSG).
   SSG used for creating blogs, landing pages and documentation.
"""

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import requests_cache
import yaml
from github import Github

requests_cache.install_cache("cache_1")


class GithubAccess:
    g = Github()


@dataclass
class Repo(GithubAccess):
    handle: str

    def __post_init__(self):
        try:
            self.repo = self.g.get_repo(self.handle)
        except:
            raise ValueError(f"Cannot read {self.handle}")

    @property
    def n_stars(self):
        return self.repo.stargazers_count

    @property
    def url(self):
        return url(self.handle)


def n_stars(handle: str):
    return Repo(handle).n_stars


def url(handle):
    return f"https://github.com/{handle}/"


def name(r):
    return r.split("/")[1]


def read_text(filename):
    return Path(filename).read_text()


def ssg_from_string(text: str):
    return yaml.load(text, Loader=yaml.SafeLoader)


def to_dicts(source_dict):
    return [
        dict(name=name(r), handle=r, lang=a["lang"], exec=a.get("exec", False))
        for r, a in source_dict.items()
    ]


def make_raw_df(dicts):
    raw_df = pd.DataFrame(dicts)
    raw_df["stars"] = raw_df.handle.map(n_stars)
    raw_df["url"] = raw_df.handle.map(url)
    raw_df = raw_df.sort_values("stars", ascending=False)
    raw_df.index = raw_df.name
    return raw_df


def md_link(word, url):
    return f"[{word}]({url})"


allowed_languages = ["go", "js", "ruby", "python", "rust", "R", "swift", "julia", "haskell"]


def get_dataframe(yaml_filename):
    text = read_text(yaml_filename)
    dicts = to_dicts(ssg_from_string(text))
    return make_raw_df(dicts)
