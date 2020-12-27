# Popularity of static site generators

Static site generators are tools to create blogs, landing pages and documentation.

![](images/plot.png)

## Dataset

<a href="https://raw.githubusercontent.com/epogrebnyak/ssg/main/data/ssg.csv"><img src="https://img.shields.io/badge/download-csv-brightgreen"></a>

|                                                                  |   '000 stars | Language   |
|------------------------------------------------------------------|--------------|------------|
| [hugo](https://github.com/gohugoio/hugo/)                        |         49.0 | go         |
| [gatsby](https://github.com/gatsbyjs/gatsby/)                    |         48.4 | js         |
| [jekyll](https://github.com/jekyll/jekyll/)                      |         41.9 | ruby       |
| [hexo](https://github.com/hexojs/hexo/)                          |         31.9 | js         |
| [vuepress](https://github.com/vuejs/vuepress/)                   |         18.1 | js         |
| [mkdocs](https://github.com/mkdocs/mkdocs/)                      |         11.3 | python     |
| [pelican](https://github.com/getpelican/pelican/)                |         10.1 | python     |
| [octopress](https://github.com/imathis/octopress/)               |          9.4 | ruby       |
| [eleventy](https://github.com/11ty/eleventy/)                    |          8.1 | js         |
| [metalsmith](https://github.com/segmentio/metalsmith/)           |          7.6 | js         |
| [middleman](https://github.com/middleman/middleman/)             |          6.7 | ruby       |
| [gridea](https://github.com/getgridea/gridea/)                   |          6.7 | js         |
| [mdBook](https://github.com/rust-lang/mdBook/)                   |          5.5 | rust       |
| [zola](https://github.com/getzola/zola/)                         |          4.7 | rust       |
| [sphinx](https://github.com/sphinx-doc/sphinx/)                  |          3.7 | python     |
| [wintersmith](https://github.com/jnordberg/wintersmith/)         |          3.5 | js         |
| [lektor](https://github.com/lektor/lektor/)                      |          3.4 | python     |
| [Cactus](https://github.com/eudicots/Cactus/)                    |          3.4 | python     |
| [Publish](https://github.com/JohnSundell/Publish/)               |          3.0 | swift      |
| [bookdown](https://github.com/rstudio/bookdown/)                 |          2.2 | r          |
| [nikola](https://github.com/getnikola/nikola/)                   |          2.1 | python     |
| [jupyter-book](https://github.com/executablebooks/jupyter-book/) |          2.0 | python     |
| [nanoc](https://github.com/nanoc/nanoc/)                         |          1.9 | ruby       |
| [cobalt.rs](https://github.com/cobalt-org/cobalt.rs/)            |          0.9 | rust       |

## Try live

<a href="https://colab.research.google.com/drive/1041e6yOyVRty5lirnbZOAU1zJ3TN77ta?usp=sharing">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

## Discussion

First thread: https://twitter.com/PogrebnyakE/status/1343105678261555200

Main ideas:

 - front-end (FE) engineers would care less about main theme for SSG
 - non-frontend people are big user group, ready-made themes are important for them
 - Next.js and Wordpress are site-building and server-side, not exactly SSG
 - people from different backgrounds adopt different tools
 - themes not transferable between SSG due to semantics
 
Use cases:

 - live book (mdbook, jupyter-book)
 - documentation
 - blog
 - langing page
 - combination of the above