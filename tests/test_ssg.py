from ssg import __version__
from ssg.stars import Repo, yaml_to_csv, create_all


def test_version():
    assert __version__ >= "0.0.0"


def test_n_forks():
    assert Repo("epogrebnyak/haskell-intro").n_forks() >= 5


import pytest


class TestFilesBase:
    yaml_doc = """
rstudio/bookdown:
  lang: r
segmentio/metalsmith:
  lang: js"""

    @pytest.fixture(autouse=True)
    def setup_method(self, tmpdir):
        self.folder = tmpdir
        self.yaml_path = tmpdir / "ssg.yaml"
        self.yaml_path.write_text(self.yaml_doc, encoding="utf-8")
        self.csv_path = tmpdir / "ssg.csv"
        self.metadata_path = tmpdir / "metadata.json"


class CreateAll(TestFilesBase):
    def test_csv_is_created(self):
        create_all(self.folder)
        assert self.csv_path.exists()

    def test_metadata_is_created(self):
        create_all(self.folder)
        assert self.metadata_path.exists()


def test_yaml_to_csv(tmpdir):
    import datetime
    import pandas as pd

    yaml_doc = """
rstudio/bookdown:
  lang: r
segmentio/metalsmith:
  lang: js"""
    yaml_path = tmpdir / "ssg.yaml"
    csv_path = tmpdir / "ssg.csv"
    columns = [
        "handle",
        "created",
        "modified",
        "stars",
        "forks",
        "open_issues",
        "lang",
        "repo_lang",
        "url",
    ]
    metadata_path = tmpdir / "metadata.json"
    yaml_path.write_text(yaml_doc, encoding="utf-8")
    df, _ = yaml_to_csv(str(tmpdir), "ssg.yaml", "ssg.csv")
    df2 = pd.read_csv(csv_path, parse_dates=["created", "modified"])
    # test dataframe equals the written csv file
    pd.testing.assert_frame_equal(
        df2.set_index("name", drop=False), df[df2.columns], check_dtype=False
    )
    # test mutable fileds will only go up
    assert df.loc["metalsmith", "stars"] >= 7736
    assert df.loc["bookdown", "stars"] >= 2985
    assert df.loc["metalsmith", "forks"] >= 667
    assert df.loc["bookdown", "forks"] >= 1135
    assert df.loc["metalsmith", "open_issues"] >= 32
    assert df.loc["bookdown", "open_issues"] >= 175
    # test the rest of fields contents
    assert df.drop(columns=["stars", "forks", "open_issues", "modified"]).to_dict() == {
        "name": {"metalsmith": "metalsmith", "bookdown": "bookdown"},
        "handle": {
            "metalsmith": "segmentio/metalsmith",
            "bookdown": "rstudio/bookdown",
        },
        "lang": {"metalsmith": "js", "bookdown": "r"},
        "exec": {"metalsmith": False, "bookdown": False},
        "twitter": {"metalsmith": "", "bookdown": ""},
        "site": {"metalsmith": "", "bookdown": ""},
        "url": {
            "metalsmith": "https://github.com/segmentio/metalsmith/",
            "bookdown": "https://github.com/rstudio/bookdown/",
        },
        "created": {
            "metalsmith": datetime.date(2014, 2, 4),
            "bookdown": datetime.date(2015, 10, 28),
        },
        "homepage": {
            "metalsmith": "https://metalsmith.io",
            "bookdown": "https://pkgs.rstudio.com/bookdown/",
        },
        "repo_lang": {"metalsmith": "JavaScript", "bookdown": "JavaScript"},
    }
