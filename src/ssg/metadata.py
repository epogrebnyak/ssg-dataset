import json
from datetime import datetime
from pathlib import Path
from typing import Union


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
