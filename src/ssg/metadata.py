from datetime import datetime
import json
from pathlib import Path
from typing import Union
from ssg import yaml_to_csv


def metadata():
    return {
        "name": "Github data for static site generators popularity",
        "created": datetime.today().date().isoformat(),
        "date_columns": ["created", "modified"],
        "repo_url": "https://github.com/epogrebnyak/ssg-dataset/",
        "data_url": "https://github.com/epogrebnyak/ssg-dataset/blob/main/data/ssg.csv",
    }


def write_metadata(folder: Union[Path, str], filename: str = "metadata.json") -> Path:
    path = Path(folder) / filename
    path.write_text(json.dumps(metadata()), encoding="utf-8")
    return path


def create_all(folder: Union[Path, str]) -> None:
    yaml_path = Path(folder) / "ssg.yaml"
    csv_path = Path(folder) / "ssg.csv"
    yaml_to_csv(yaml_path, csv_path)
    print("Wrote", csv_path)
    metadata_path = write_metadata(folder)
    print("Wrote", metadata_path)
