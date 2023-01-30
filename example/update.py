from pathlib import Path

from ssg import yaml_to_csv

data_folder = Path(__name__).resolve().parent / "data"
yaml_path = data_folder / "ssg.yaml"
csv_path = data_folder / "ssg.csv"
yaml_to_csv(yaml_path, csv_path)
