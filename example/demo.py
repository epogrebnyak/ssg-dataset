import datetime
import tempfile
from pathlib import Path
from typing import Dict, Optional

import pandas as pd

from ssg.github import get_repo_state_from_handle
from ssg.stars import extract_yaml, make_dataframe_from_ssg, to_ssg_list, yaml_to_csv

rs = get_repo_state_from_handle("tighten/jigsaw")
print(rs)
