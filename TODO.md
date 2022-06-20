Fixes
=====

Easy / priority:

- [ ] validate programming language as in https://pydantic-docs.helpmanual.io/usage/validators/
- [ ] check date in SSG class and change `date_only()`

More difficult:

- [ ] documentation: build sphinx docs for the package, show on Github Pages
- [ ] add pyright check to CI pipeline (may not install with poetry)

Bugs:

- [ ] release date in streamlit app not updated 

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
