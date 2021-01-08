from pathlib import Path

from ssg import yaml_to_csv

data_folder = Path(__name__).parent / "data"
yaml_to_csv(str(data_folder))
