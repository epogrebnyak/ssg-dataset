from datetime import date

from ssg.github import date_only
from ssg.stars import get_repo_state_from_handle


def test_get_repo_state_from_handle():
    rs = get_repo_state_from_handle("rstudio/bookdown")
    assert rs.repo_lang == "JavaScript"
    assert rs.url == "https://github.com/rstudio/bookdown/"
    assert rs.homepage == "https://pkgs.rstudio.com/bookdown/"
    assert rs.created == date(2015, 10, 28)
    assert rs.modified >= date(2022, 6, 14)
    assert rs.stars >= 2985  # we assume number of stars does not decrease
    assert rs.forks >= 1135  # we assume number of forks also does not decrease
    assert isinstance(
        rs.open_issues, int
    )  # number of issues is known to decrease, so we check only type (integer)


def test_date_only_on_isoformat_with_z_passes():
    assert date_only("2021-03-15T17:19:47Z") == date(2021, 3, 15)
    assert date_only("2022-06-22T12:11:55Z") == date(2022, 6, 22)
    assert date_only("2022-06-22T12:32:55Z") == date(2022, 6, 22)
