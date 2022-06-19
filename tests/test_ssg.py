import datetime

import pandas as pd
import pytest

from ssg import __version__
from ssg.stars import Repo, create_all, yaml_to_csv, extract_yaml, get_repo_state


def test_version():
    assert __version__ >= "0.0.0"


def test_read_item():
    from ssg.stars import SSG, read_item

    s = SSG(
        name="bookdown", github_handle="rstudio/bookdown", lang="r", site="bookdown.org"
    )
    s2 = read_item("rstudio/bookdown", {"lang": "r", "site": "bookdown.org"})
    assert s == s2


def test_repo_state():
    rs = get_repo_state("rstudio/bookdown")
    assert rs.repo_lang == "JavaScript"
    assert rs.url == "https://github.com/rstudio/bookdown/"
    assert rs.homepage == "https://pkgs.rstudio.com/bookdown/"
    assert rs.created == "2015-10-28"
    assert rs.modified >= "2022-06-14"
    assert rs.stars >= 2985
    assert rs.forks >= 1135
    assert isinstance(rs.open_issues, int)


def test_extract_yaml():
    yaml_doc = """
rstudio/bookdown:
    lang: r
segmentio/metalsmith:
    lang: js
"""
    assert extract_yaml(yaml_doc) == {
        "rstudio/bookdown": {"lang": "r"},
        "segmentio/metalsmith": {"lang": "js"},
    }


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


class Test_create_all(TestFilesBase):
    def test_csv_is_created(self):
        create_all(self.folder)
        assert self.csv_path.exists()

    def test_metadata_is_created(self):
        create_all(self.folder)
        assert self.metadata_path.exists()


class Test_yaml_to_csv(TestFilesBase):
    columns = [
        "github_handle",
        "created",
        "modified",
        "stars",
        "forks",
        "open_issues",
        "lang",
        "repo_lang",
        "url",
    ]

    def test_we_write_exact_data(self):
        df, _ = yaml_to_csv(self.folder, "ssg.yaml", "ssg.csv", self.columns)
        df2 = pd.read_csv(self.csv_path, parse_dates=["created", "modified"])
        pd.testing.assert_frame_equal(
            df2.set_index("name", drop=False), df[df2.columns], check_dtype=False
        )

    def test_dataframe_immutable_data(self):
        df, _ = yaml_to_csv(self.folder, "ssg.yaml", "ssg.csv", self.columns)
        assert df.loc["metalsmith", "stars"] >= 7736
        assert df.loc["bookdown", "stars"] >= 2985
        assert df.loc["metalsmith", "forks"] >= 667
        assert df.loc["bookdown", "forks"] >= 1135
        assert df.loc["metalsmith", "open_issues"] >= 32
        assert df.loc["bookdown", "open_issues"] >= 175

    def test_dataframe_mutable_data(self):
        df, _ = yaml_to_csv(self.folder, "ssg.yaml", "ssg.csv", self.columns)
        assert df.drop(
            columns=["stars", "forks", "open_issues", "modified"]
        ).to_dict() == {
            "name": {"metalsmith": "metalsmith", "bookdown": "bookdown"},
            "github_handle": {
                "metalsmith": "segmentio/metalsmith",
                "bookdown": "rstudio/bookdown",
            },
            "lang": {"metalsmith": "js", "bookdown": "r"},
            "exec": {"metalsmith": None, "bookdown": None},
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
            "comment": {"bookdown": "", "metalsmith": ""},
        }
