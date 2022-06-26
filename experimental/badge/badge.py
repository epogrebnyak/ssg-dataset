from dataclasses import dataclass 
from pybadges import badge
from typing import Optional

@dataclass
class Badge:
    left_text: str
    right_text: str
    right_color: str
    left_color: str = '#555'

    def image(self):
        return badge(
        left_text = self.left_text,
        right_text = self.right_text,
        left_color = self.left_color,
        right_color = self.right_color,
    )

    def image_with_link(self, url):
        return badge(
        left_text = self.left_text,
        right_text = self.right_text,
        right_link = url,
        left_link = url,
        left_color = self.left_color,
        right_color = self.right_color,
    )

def generate_badge(left_text: str,
                   right_text: str,
                   right_color: str,
                   link: Optional[str] = None,
                   left_color: str = '#555'
                   ) -> str:
    svg = badge(
        left_text = left_text,
        right_text = right_text,
        right_link = link,
        left_link = link,
        left_color = left_color,
        right_color = right_color,
    )
    if link:
        return svg
    else:
        return svg.replace('xlink:', '')

print(Badge("SSG", "43", "gray").image_with_link("http://www.w3.org/2000/svg"))