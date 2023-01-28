import streamlit as st

st.write(
    """## My favorite tools

Several documentation engines I have worked with:

**Doks for Hugo**: Enhanced theme for the Hugo static site generator
-- extremely fast page rendering, built-in YouTube and Twitter shortcodes, 
and allows to combine landing page, documentation and a blog view. 
May require a bit of learning to get started.

**mkdocs-material**: Constantly progressing with new features, and is very popular 
for building documentation. Has built-in color themes, and very easy to start with. 
It also has buttons, callouts and a built-in blog feature.

**jupyterbook**: Designed to bundle computational notebooks, based on Sphinx.
Can render PDFs as output, and has a selection of buttons and grids.

**VitePress**: Very clean look and layout and very easy to start using, even not for 
JavaScript user. Wish I can customize code blocks to use a light theme.

**MdBook**: Native for Rust documentation. Quick to start with, has a strict design, 
and supports runnable code snippets in Rust.

The ideal SSG has:
 - speed and shortcodes from Hugo
 - cleanliness of Vitepress
 - color schemes and clarity from mkdocs-material
 - runnable code snippets as in MdBook
 - easy access to design elements as in Jupyterbook
 - grids, blog, and easy setup for landing page
 - can start working quick.
"""
)
