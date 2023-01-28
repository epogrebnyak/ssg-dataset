from pathlib import Path

from ssg import yaml_to_csv

data_folder = Path(__name__).resolve().parent / "data"
yaml_to_csv(yaml_path=data_folder / "ssg2.yaml", csv_path=data_folder / "ssg.csv")
