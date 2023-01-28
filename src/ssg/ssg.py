# pylint:disable=missing-function-docstring,missing-class-docstring,import-error

from pathlib import Path
from typing import List, Union

import yaml

# from pydantic import validator
from pydantic.dataclasses import dataclass
import pandas as pd  # type: ignore

from ssg.github import get_repo_state_from_handle

__all__ = ["make_generators_list", "from_yaml"]

YAML_DOC = """
---
elm:
 - alexkorban/elmstatic
Go:
 - h-enk/doks
 - gohugoio/hugo
Haskell:
 - digitallyinduced/ihp
 - jaspervdj/hakyll
Java:
 - jbake-org/jbake
JavaScript:
 - gatsbyjs/gatsby
 - hexojs/hexo
 - vuejs/vuepress
 - vuejs/vitepress
 - nuxt/content
 - withastro/astro
 - 11ty/eleventy
 - ionic-team/stencil
 - getgridea/gridea
 - segmentio/metalsmith
 - shuding/nextra
 - jnordberg/wintersmith
 - scullyio/scully
Julia:
 - tlienart/Franklin.jl
PHP:
 - tighten/jigsaw
Python:
 - mkdocs/mkdocs
 - squidfunk/mkdocs-material
 - getpelican/pelican
 - sphinx-doc/sphinx
 - lektor/lektor
 - eudicots/Cactus
 - fastai/fastpages
 - executablebooks/jupyter-book
 - getnikola/nikola
R:
 - rstudio/bookdown
Ruby:
 - jekyll/jekyll
 - imathis/octopress
 - middleman/middleman
 - nanoc/nanoc
 - bridgetownrb/bridgetown
Rust:
 - rust-lang/mdBook
 - getzola/zola
 - cobalt-org/cobalt.rs
Swift:
 - JohnSundell/Publish
"""

from enum import Enum


class Provider(Enum):
    Github = "github"
    Gitlab = "gitlab"


#


@dataclass
class Repo:
    handle: str

    def __post_init__(self):
        if "/" not in self.handle:
            raise ValueError(f"Handle must contain '/'. Got: {self.handle}")

    # FIXME: does not work with inherited class
    #    @validator("github_handle")
    #    def github_handle_field_must_contain_slash(cls, value: str) -> str:
    #        if "/" not in value:
    #            raise ValueError(f"Field github_handle must contain '/'. Got: {value}")
    #        return value

    @property
    def name(self):
        return self.handle.split("/")[1]


@dataclass
class Github(Repo):
    pass


@dataclass
class SSG:
    repo: Repo
    lang: str

    def to_dict(self):
        return dict(name=self.repo.name, github_handle=self.repo.handle, lang=self.lang)


def to_dict(ssg: SSG):
    """Merge two dictionaries."""
    return {**ssg.to_dict(), **get_state_dict(ssg)}


def get_state_dict(ssg: SSG):
    return get_repo_state_from_handle(ssg.repo.handle).__dict__


def read_text(filename) -> str:
    text = Path(filename).read_text(encoding="utf-8")
    return text if text else ""  # prevent returning None


def extract_yaml(text: str):
    return yaml.load(text, Loader=yaml.SafeLoader)


def make_generators_list(src_dict) -> List[SSG]:
    return [
        SSG(Github(handle), lang)
        for lang, handles in src_dict.items()
        for handle in handles
    ]


def from_yaml(path) -> List[SSG]:
    return make_generators_list(extract_yaml(read_text(path)))


def to_dataframe(ssg_list: List[SSG]) -> pd.DataFrame:
    df = pd.DataFrame([to_dict(ssg) for ssg in ssg_list])
    for key in ["created", "modified"]:
        df[key] = df[key].map(lambda x: pd.to_datetime(x).date())
    return df.sort_values("stars", ascending=False)


def yaml_to_csv(yaml_path: Union[Path, str], csv_path: Union[Path, str]):
    """Accept list of static site generators from YAML file
    at *yaml_path*, collect and write statistics to CSV file
    at *csv_path*."""
    ssg_list = from_yaml(yaml_path)
    df = to_dataframe(ssg_list)
    columns = [
        "name",
        "stars",
        "forks",
        "open_issues",
        "created",
        "modified",
        "lang",
        "repo_lang",
        "github_handle",
        "url",
        "homepage",
    ]
    df[columns].to_csv(csv_path, index=False)
    return df[columns]
