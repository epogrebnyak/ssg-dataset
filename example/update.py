from pathlib import Path

from ssg import yaml_to_csv
from ssg.metadata import write_metadata

data_folder = Path(__name__).resolve().parent / "data"
yaml_to_csv(yaml_path=data_folder / "ssg.yaml", csv_path=data_folder / "ssg.csv")
write_metadata(data_folder)
