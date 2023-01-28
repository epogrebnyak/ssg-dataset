# from ssg.stars import SSG, create_all, extract_yaml, yaml_to_csv

from ssg import yaml_to_csv

YAML_DOC = """
---
PHP:
 - tighten/jigsaw
Python:
 - mkdocs/mkdocs
 - squidfunk/mkdocs-material
"""

from ssg.ssg import extract_yaml, Github
import pytest


def test_validator_for_github_handle_raises_error_without_slash():
    with pytest.raises(ValueError):
        Github(handle="gatsbyjs_gatsby")


def test_extract_yaml_is_runnable():
    assert extract_yaml(YAML_DOC) == {
        "PHP": ["tighten/jigsaw"],
        "Python": ["mkdocs/mkdocs", "squidfunk/mkdocs-material"],
    }


@pytest.fixture
def yaml_path_str(tmp_path):
    doc = """
R:
- rstudio/bookdown
JavaScript:
- segmentio/metalsmith"""
    yaml_path = tmp_path / "ssg.yaml"
    yaml_path.write_text(doc, encoding="utf-8")
    yield str(yaml_path)


@pytest.fixture
def csv_path_str(tmp_path):
    return str(tmp_path / "ssg.csv")


@pytest.fixture
def filled_csv_path(yaml_path_str, csv_path_str):
    yaml_to_csv(yaml_path_str, csv_path_str)
    yield csv_path_str


class TestDataframe:
    @pytest.fixture(autouse=True)
    def setup_method(self, yaml_path_str, csv_path_str):
        import pandas as pd

        yaml_to_csv(yaml_path_str, csv_path_str)
        self.df = pd.read_csv(csv_path_str)

    def test_immutable_columns(self):
        cols = "name,created,lang,repo_lang,github_handle,url,homepage".split(",")
        assert self.df[cols].to_csv().split() == [
            ",name,created,lang,repo_lang,github_handle,url,homepage",
            "0,metalsmith,2014-02-04,JavaScript,JavaScript,segmentio/metalsmith,https://github.com/segmentio/metalsmith/,https://metalsmith.io",
            "1,bookdown,2015-10-28,R,JavaScript,rstudio/bookdown,https://github.com/rstudio/bookdown/,https://pkgs.rstudio.com/bookdown/",
        ]

    def test_mutable_columns_with_dict(self):
        import datetime

        cols = "github_handle lang repo_lang url created homepage".split()
        assert self.df.set_index("name").loc[:, cols].to_dict() == {
            "github_handle": {
                "metalsmith": "segmentio/metalsmith",
                "bookdown": "rstudio/bookdown",
            },
            "lang": {"metalsmith": "JavaScript", "bookdown": "R"},
            "repo_lang": {"metalsmith": "JavaScript", "bookdown": "JavaScript"},
            "url": {
                "metalsmith": "https://github.com/segmentio/metalsmith/",
                "bookdown": "https://github.com/rstudio/bookdown/",
            },
            "created": {
                "metalsmith": "2014-02-04",
                "bookdown": "2015-10-28",
            },
            "homepage": {
                "metalsmith": "https://metalsmith.io",
                "bookdown": "https://pkgs.rstudio.com/bookdown/",
            },
        }

    def test_mutable_columns(self):
        df = self.df.set_index("name")
        assert df.loc["metalsmith", "stars"] >= 7735
        assert df.loc["bookdown", "stars"] >= 2985
        assert df.loc["metalsmith", "forks"] >= 600  # forks may decrease too
        assert df.loc["bookdown", "forks"] >= 1135
        assert df.loc["metalsmith", "open_issues"] >= 0
        assert df.loc["bookdown", "open_issues"] >= 0
