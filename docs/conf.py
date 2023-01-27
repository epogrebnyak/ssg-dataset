"""Sphinx configuration."""
from datetime import datetime

year = datetime.now().year

project = "ssg"
author = "Evgeniy Pogrebnyak"
copyright = f"{year}, {author}"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.autosummary", "myst_parser"]
autodoc_typehints = "description"
html_theme = "pydata_sphinx_theme"
exclude_patterns = ["site/*"]

html_theme_options = {"github_url": "https://github.com/epogrebnyak/ssg-dataset/"}
