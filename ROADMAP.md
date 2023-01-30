TIL

Created a multipage version of a Streamlit app, that demonstrates several
charts about static site generators (SSG) popularity (Hugo, Gatsby, Jekyll, sphinx, etc).

The dataset is collected from Github API and has repo names, stars, forks, issues,
create and modify dates. There is Python package to process this data,
that results in a CSV file.

The CSV file is at project repo, the app reads the data,
and lays out several charts - by programming language,
issues vs forks, years project is running and several project
without recent commits.

Some things I learned while creating the app:

- Multipage option is great, helps to focus on parts of content, each page is shorter and
  tells one thing.
- I used ChatGPT to come up with an icon for the page, which really saved time.
  I asked about what icons could I use and where the icon looked poorly on actual site,
  asked again for more options. Much more satisfying than browsing emoji tables for a fun
  pictogram.
- I wanted a badge with a number of SSG in a dataset, that I ended up creating locally
  with `npm badge-maker`. There was also some code with `pybadges`, but `badge-maker`
  allowed to use a one-liner (you can check `badge` command in `justfile`).
- I relay poetry project version number to a Github tag, and make a release badge based on this tag
  though shields API.
- Someone mentioned it is nice to have Github colors for programming language, which I did.
  (`palette()` function).

Open questions:

- I used `st.session_state` to communicate the CSV data between pages, initialised at homepage.
  The state was not really changing, just some way to communicate my dataset between pages.
  The only discomfort is when a browser is pointing to a sub-page after restart, there is an error
  about no data available. Perhaps this not a likely scenario for a hosted page (the user always comes to home page, I assume).
- My initial solution attempt was to use `data.py` and import it as a data store to everypage,
  which did not work well -- how to make it discoverable by home page and pages, make data actually persist and guarantee I'm not reading the CSV repeatedly -- I could not resolve that quickly
  and `st.session_state` seemed a quicker solution.
- If I had access to page tree, I think a footer at each page made sense, what section to read next.
  Also some global header and footer can be useful, but probably not a priority for streamlit as a library.

---

# Fixes

## Easy

...

## Medium

- [ ] citation and new zenodo version
- [x] cleanup examples folder
- [-] contributor guide for onboarding

## More difficult

...

# Bugs

...

# Wontfix

...

# Enhancements and new features

Nicer badge for streamlit (issue #16):

- [x] total SSG counted + badge
- [x] badge class for Streamlit

Get more data:

- [ ] stars history (issue #1)
- [ ] migration matrix (issue #8)

More charts:

- [ ] stars per project year chart
- [ ] heatmap mekko chart
- [ ] history timeline chart

Enhancements:
`

- [ ] сommand line interface
- [ ] can use typing check on dataframe https://pandera.readthedocs.io/en/stable/
- [x] try https://blog.streamlit.io/introducing-multipage-apps/

# Discussion

- Framework-based SSG (JavaScript), eg [Next, Nuxt](https://ssg-build-performance-tests.netlify.app/), are not listed (commented out in README)
- We cannot list [Antora from Gitlab](https://gitlab.com/antora/antora), our URL system is for Github
