from pathlib import Path

from ssg import create_all

data_folder = Path(__name__).parent / "data"
create_all(data_folder)
