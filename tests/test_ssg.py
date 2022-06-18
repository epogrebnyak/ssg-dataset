from ssg import __version__
from ssg.stars import Repo, yaml_to_csv


def test_version():
    assert __version__ >= "0.0.0"


def test_n_forks():
    assert Repo("epogrebnyak/haskell-intro").n_forks() >= 5


def test_yamk_to_csv(tmpdir):
    import datetime

    yaml_doc = """
rstudio/bookdown:
  lang: r
segmentio/metalsmith:
  lang: js"""
    yaml_path = tmpdir / "ssg.yaml"
    yaml_path.write_text(yaml_doc, encoding="utf-8")
    df = yaml_to_csv(str(tmpdir), "ssg.yaml", "ssg.csv")
    assert (df.loc[["metalsmith", "bookdown"], "stars"].to_numpy() >= (7736, 2985)).all()
    assert df.to_dict("split") == {
        "columns": [
            "name",
            "handle",
            "lang",
            "exec",
            "twitter",
            "site",
            "url",
            "modified",
            "stars",
            "forks",
            "open_issues",
            "created",
            "homepage",
            "repo_lang",
        ],
        "data": [
            [
                "metalsmith",
                "segmentio/metalsmith",
                "js",
                False,
                "",
                "",
                "https://github.com/segmentio/metalsmith/",
                datetime.date(2022, 6, 10),
                7736,
                667,
                32,
                datetime.date(2014, 2, 4),
                "https://metalsmith.io",
                "JavaScript",
            ],
            [
                "bookdown",
                "rstudio/bookdown",
                "r",
                False,
                "",
                "",
                "https://github.com/rstudio/bookdown/",
                datetime.date(2022, 6, 14),
                2985,
                1135,
                175,
                datetime.date(2015, 10, 28),
                "https://pkgs.rstudio.com/bookdown/",
                "JavaScript",
            ],
        ],
        "index": ["metalsmith", "bookdown"],
    }
