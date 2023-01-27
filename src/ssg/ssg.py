# pylint:disable=missing-function-docstring,missing-class-docstring,import-error

from pathlib import Path

import yaml
from pydantic import validator
from pydantic.dataclasses import dataclass

from github import get_repo_state_from_handle

__all__ = ["make_generators_list", "from_file"]

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


@dataclass
class Repo:
    handle: str

    @property
    def name(self):
       return self.handle.split("/")[1]


@dataclass
class Github(Repo):
    pass

#    @validator("github_handle")
#    def github_handle_field_must_contain_slash(cls, value: str) -> str:
#        if "/" not in value:
#            raise ValueError(f"Field github_handle must contain '/'. Got: {value}")
#        return value

@dataclass
class SSG:
    repo: Repo
    lang: str

    def to_dict(self):
        return dict(name=self.repo.name, github_handle=self.repo.handle, lang=self.lang)

def to_dict(ssg: SSG):
      """Merge two dictionaries."""
      return {
          **ssg.to_dict(),
          **get_state_dict(ssg)
      }


def get_state_dict(ssg: SSG):
    return get_repo_state_from_handle(ssg.repo.handle).__dict__


def read_text(filename) -> str:
    text = Path(filename).read_text(encoding="utf-8")
    return text if text else ""  # prevent returning None


def extract_yaml(text: str):
    return yaml.load(text, Loader=yaml.SafeLoader)


def make_generators_list(yaml_str=YAML_DOC):
    return [
        SSG(Github(handle), lang)
        for lang, handles in extract_yaml(yaml_str).items()
        for handle in handles
    ]


def from_file(path):
    return to_dataframe(make_generators_list(extract_yaml(read_text(path))))


SSG_LIST = make_generators_list()

import pandas as pd  # type: ignore
from typing import List

def to_dataframe(ssg_list: List[SSG]) -> pd.DataFrame:
    df = pd.DataFrame([to_dict(ssg) for ssg in ssg_list])
    for key in ["created", "modified"]:
        df[key] = df[key].map(lambda x: pd.to_datetime(x).date())
    return df.sort_values("stars", ascending=False)


ssg_list = from_file("../data/ssg2.yaml")
print(ssg_list)
#df = to_dataframe(ssg_list)
#df.to_csv("../data/ssg.csv")

#print(to_dict(SSG_LIST[0]))
#print(to_dataframe(SSG_LIST[0:5]))

def yaml_to_csv(
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
