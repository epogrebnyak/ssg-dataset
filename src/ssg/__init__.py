"""Popularity of static site generators (SSG).

Creates a dataset in a CSV file based on listing of Github repos in YAML file.

Example:

  from ssg import yaml_to_csv

  yaml_to_csv("data/ssg.yaml", "data/ssg.csv")
"""

from .cache import has_token
from .ssg import from_yaml, to_dataframe, yaml_to_csv
