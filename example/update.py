from pathlib import Path

from ssg import get_dataframe

data_folder = Path(__name__).parent / "data"
df = get_dataframe(data_folder / "ssg.yaml")
df[["stars", "forks", "lang", "url"]].to_csv(data_folder / "ssg.csv")
