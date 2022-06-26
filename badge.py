from pybadges import badge, text_measurer
from typing import Optional


def badge_generate(
    left_text: str,
    right_text: str,
    left_link: Optional[str] = None,
    right_link: Optional[str] = None,
    whole_link: Optional[str] = None,
    logo: Optional[str] = None,
    left_color: str = '#555',
    right_color: str = '#007ec6',
    measurer: Optional[text_measurer.TextMeasurer] = None,
    embed_logo: bool = False,
    whole_title: Optional[str] = None,
    left_title: Optional[str] = None,
    right_title: Optional[str] = None,
    id_suffix: str = '',
) -> str:
    svg = badge(
        left_text = left_text,
        right_text = right_text,
        left_link = left_link,
        right_link = right_link,
        whole_link = whole_link,
        logo = logo,
        left_color = left_color,
        right_color = right_color,
        measurer = measurer,
        embed_logo = embed_logo,
        whole_title = whole_title,
        left_title = left_title,
        right_title = right_title,
        id_suffix = id_suffix,
    )

    if left_link is not None or right_link is not None or whole_link is not None:
        return svg.replace('xlink:', '')
    return svg

