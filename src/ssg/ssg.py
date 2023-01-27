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
JavaScript (frameworks):
 - gatsbyjs/gatsby
JavaScript:
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
 - tlienart/Franklin.jl	Julia	Julia
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

from pydantic.dataclasses import dataclass
from typing import List

@dataclass 
class SSG:
    github: str
    lang: str

from pathlib import Path
import yaml

def read_text(filename) -> str:
    text = Path(filename).read_text(encoding="utf-8")
    return text if text else ""  # prevent returning None

def extract_yaml(text: str):
    return yaml.load(text, Loader=yaml.SafeLoader)

def make_generators_list(yaml_str=YAML_STR):
    for lang, handles in extract_yaml(yaml_str).items():
        for handle in handles:
            yield SSG(handle, lang)

SSG_LIST = list(make_generators_list())

from github import get_repo_state

print(SSG_LIST[0].handle)
print(get_repo_state(SSG_LIST[0].handle))

#s = SSG("alexkorban/elmstatic", "elm")
#print([SSG(*row) for row in reader if row])
