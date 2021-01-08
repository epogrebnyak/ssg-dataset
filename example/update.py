from pathlib import Path

from ssg import get_dataframe

data_folder = Path(__name__).parent / "data"
src = data_folder / "ssg.yaml"
dst = data_folder / "ssg.csv"
df = get_dataframe(src)
df[["stars", "forks", "lang", "url"]].to_csv(dst)
