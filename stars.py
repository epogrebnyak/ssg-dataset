"""Popularity statisctics for SSG - static site generators.
   Used as blogs, landing pages and documentation tools
   
   Install dependencies:
     pip3 install PyGithub requests_cache pandas
"""

from github import Github
import pandas as pd
import requests_cache
from dataclasses import dataclass
import yaml

requests_cache.install_cache('cache_1')

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

def ssg_from_string(s):
    return yaml.load(s, Loader=yaml.SafeLoader)

def to_dicts(source_dict):
    return [dict(name=name(r), 
                 handle=r, 
                 lang=a['lang'], 
                 exec=a.get('exec', False)) for r, a in source_dict.items()]

def make_raw_df(dicts):
    raw_df = pd.DataFrame(dicts)
    raw_df['stars']=raw_df.handle.map(n_stars)
    raw_df['url']=raw_df.handle.map(url)
    raw_df = raw_df.sort_values("stars",ascending=False)
    raw_df.index = raw_df.name
    return raw_df 

def md_link(word, url):
    return f"[{word}]({url})"
   

allowed_languages = ['go', 'js', 'ruby', 'python', 'rust']
    
if __name__== "__main__":
    
    doc="""
    gohugoio/hugo:
      lang: go
      exec: True
    jekyll/jekyll:
      lang: ruby
    gatsbyjs/gatsby:
      lang: js
    hexojs/hexo:
      lang: js
    vuejs/vuepress:
      lang: js  
    mkdocs/mkdocs:
      lang: python  
    getpelican/pelican:
      lang: python
    11ty/eleventy:
      lang: js
    sphinx-doc/sphinx:
      lang: python
    getnikola/nikola:
      lang: python    
    getzola/zola:
      lang: rust
      exec: True    
    rust-lang/mdBook:
      lang: rust    
      exec: True
    executablebooks/jupyter-book:
      lang: python  
    """
    
    dicts = to_dicts(ssg_from_string(doc))
    raw_df = make_raw_df(dicts)
    df = raw_df[['stars', 'lang', 'url']]
    df['stars'] = df.stars.divide(1000).round(1)
    df.index=raw_df.apply(lambda x: md_link(x.name, x.url), result_type='expand', axis=1)  
    del df['url']
    print(raw_df)
    