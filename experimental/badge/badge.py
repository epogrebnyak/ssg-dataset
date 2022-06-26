from dataclasses import dataclass
from pybadges import badge
from typing import Optional
from pathlib import Path


@dataclass
class Badge:
    left_text: str
    right_text: str
    right_color: str
    left_color: str = "#555"

    def image(self) -> str:
        return badge(**self.__dict__)

    def image_with_link(self, url: str) -> str:
        svg = badge(**self.__dict__, right_link=url, left_link=url)
        return svg.replace("a xlink:href", "a href")

    def save(self, path: Path, url: Optional[str] = None):
        if url:
            svg = self.image_with_link(url)
        else:
            svg = self.image()
        path.write_text(svg)


b = Badge("SSG", "43", "pink")
url_ = "http://www.nba.com"
this_dir = Path(__file__).resolve().parent

assert b.image().startswith("<svg")
assert "nba.com" in b.image_with_link(url_)

b.save(this_dir / "count.svg")
b.save(this_dir / "count2.svg", url_)
