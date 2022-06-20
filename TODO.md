Fixes
=====

## Easy

- [ ] validate programming language as in https://pydantic-docs.helpmanual.io/usage/validators/
- [ ] check date in SSG class and change `date_only()`

## More difficult

- [ ] documentation: build sphinx docs for the package, show on Github Pages
- [ ] add pyright check to CI pipeline (may not install with poetry)
- [ ] can use typing check on dataframe https://pandera.readthedocs.io/en/stable/

## Bugs

- [ ] release date in streamlit app not updated 
- [ ] pytest does not run on Codespaces https://github.com/LukeMathWalker/linfa-python/issues/3#issuecomment-1160007455

Wontfix
=======

- programming language list is hardcoded in stars.py

Enhancement
===========

- [ ] Github colors for programming languages, use https://github.com/ozh/github-colors/blob/master/colors.json (issue)
- [ ] Proofread text on streamlit page

New features
============

- [ ] stars history (issue)
- [ ] migration matrix (issue)

Discussion
==========

- Framework-based SSG (JavaScript), eg [Next, Nuxt](https://ssg-build-performance-tests.netlify.app/), are not listed (commented out in README) 
- We cannot list [Antora from Gitlab](https://gitlab.com/antora/antora), our URL system is for Github
