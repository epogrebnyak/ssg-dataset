from ssg.stars import get_repo_state_from_handle


def test_get_repo_state_from_handle():
    rs = get_repo_state_from_handle("rstudio/bookdown")
    assert rs.repo_lang == "JavaScript"
    assert rs.url == "https://github.com/rstudio/bookdown/"
    assert rs.homepage == "https://pkgs.rstudio.com/bookdown/"
    assert rs.created == "2015-10-28"
    assert rs.modified >= "2022-06-14"
    assert rs.stars >= 2985
    assert rs.forks >= 1135
    assert isinstance(rs.open_issues, int)
