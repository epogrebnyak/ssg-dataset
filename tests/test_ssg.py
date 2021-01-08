from ssg import __version__
from ssg.stars import n_forks


def test_version():
    assert __version__ >= "0.0.0"


def test_n_forks():
    assert n_forks("epogrebnyak/haskell-intro") >= 5
