import streamlit as st

st.write(
    """## My favorite tools

Several documentation engines I have worked with:

[Doks for Hugo][doks]: Enhanced theme for the Hugo static site generator
-- extremely fast page rendering, built-in YouTube and Twitter shortcodes,
and allows to combine landing page, documentation and a blog view.
May require a bit of learning to get started.

[mkdocs-material][mkdocs-material]: Constantly progressing with new features,
and is very popular for building documentation. Has built-in color themes,
and very easy to start with. It also has buttons, callouts and a built-in blog feature.

[Jupyter Book][jupyterbook]: Designed to bundle computational notebooks, based on Sphinx.
Can render PDFs as output, and has a selection of buttons and grids.

[VitePress][vitepress]: Very clean look and layout and very easy to start using,
even not for usual JavaScript user. Wish I can customize code blocks to use a light theme.

[mdBook][mdbook]: Native for Rust documentation. Quick to start with,
has a strict and consistent design, and supports runnable code snippets in Rust.

[mdbook]: https://github.com/rust-lang/mdBook
[vitepress]: https://github.com/vuejs/vitepress
[jupyterbook]: https://github.com/executablebooks/jupyter-book
[mkdocs-material]: https://squidfunk.github.io/mkdocs-material/
[doks]: https://github.com/h-enk/doks

The ideal SSG has:
 - speed and shortcodes from Hugo
 - cleanliness of Vitepress
 - color schemes and clarity from mkdocs-material
 - runnable code snippets as in mdBook
 - buttons and design elements as in Jupyter Book
 - grids, blog, and a setup for landing page
 - easy to start working with and extend later.
"""
)
