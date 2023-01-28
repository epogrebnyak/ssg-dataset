from dataclasses import dataclass
import pandas as pd
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
        return badge(
            left_text=self.left_text,
            right_text=self.right_text,
            right_color=self.right_color,
            left_color=self.left_color,
        )

    def image_with_link(self, url: str) -> str:
        svg = badge(
            left_text=self.left_text,
            right_text=self.right_text,
            right_color=self.right_color,
            left_color=self.left_color,
            right_link=url,
            left_link=url,
        )
        return svg.replace("a xlink:href", "a href")

    def save(self, path: Path, url: Optional[str] = None):
        if url:
            svg = self.image_with_link(url)
        else:
            svg = self.image()
        path.write_text(svg)


df = pd.read_csv("data/ssg.csv", parse_dates=["created", "modified"])
n = len(df)
b = Badge("SSG", str(n), "brightgreen")
b.save(Path(__file__).resolve().parent / "ssg_count.svg")
print(f"Created badge for {n} SSG.")
