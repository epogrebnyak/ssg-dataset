Fixes
=====

## Easy

- [ ] validate programming language as in https://pydantic-docs.helpmanual.io/usage/validators/
- [ ] check date in SSG class and change `date_only()`
- [ ] citation and new zenodo version

## More difficult

- [ ] documentation: build sphinx docs for the package, show on Github Pages
- [ ] add pyright check to CI pipeline (may not install with poetry)
- [ ] can use typing check on dataframe https://pandera.readthedocs.io/en/stable/

## Bugs

None at the moment.

Wontfix
=======

- programming language list is hardcoded in stars.py

Enhancements and new features
=============================

- [ ] stars history (issue)
- [ ] migration matrix (issue)
- [ ] total SSG counted + badge
- [ ] try https://blog.streamlit.io/introducing-multipage-apps/
- [ ] stars per project year chart





Discussion
==========

- Framework-based SSG (JavaScript), eg [Next, Nuxt](https://ssg-build-performance-tests.netlify.app/), are not listed (commented out in README) 
- We cannot list [Antora from Gitlab](https://gitlab.com/antora/antora), our URL system is for Github
