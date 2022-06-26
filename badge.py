from pybadges import badge
from typing import Optional


def badge_generate(left_text: str,
                   right_text: str,
                   right_color,
                   link: Optional[str] = None,
                   logo: Optional[str] = None,
                   left_color: str = '#555'
                   ) -> str:
    svg = badge(
        left_text = left_text,
        right_text = right_text,
        right_link = link,
        left_link = link,
        logo = logo,
        left_color = left_color,
        right_color = right_color,
    )
    if link is not None:
        return svg.replace('xlink:', '')
    return svg

