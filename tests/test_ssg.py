from ssg import __version__
from ssg.stars import Repo


def test_version():
    assert __version__ >= "0.0.0"


def test_n_forks():
    assert Repo("epogrebnyak/haskell-intro").n_forks() >= 5
