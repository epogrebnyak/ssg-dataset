"""Popularity of static site generators (SSG).

Creates a dataset in a CSV file based on listing of SSG Github addresses (handles) in YAML file.

Example:

  yaml_to_csv_by_file("data/ssg.yaml", "data/ssg.csv")
  create_all("data")

"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Union

import pandas as pd  # type: ignore


__all__ = ["yaml_to_csv_by_file", "create_all"]

import pandas as pd  # type: ignore
