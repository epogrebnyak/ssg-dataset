# from ssg.stars import SSG, create_all, extract_yaml, yaml_to_csv

from ssg import yaml_to_csv

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

from ssg.ssg import extract_yaml


def test_extract_yaml_is_runnable():
    assert extract_yaml(YAML_DOC)
