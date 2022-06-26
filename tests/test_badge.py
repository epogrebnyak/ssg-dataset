from badge import badge_generate


def test_badge_generate_on_static_input_all_svg_equal() -> None:
    correct_svg = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="73.5" height="20"><linearGradient id="smooth" x2="0" y2="100%"><stop offset="0" stop-color="#bbb" stop-opacity=".1"/><stop offset="1" stop-opacity=".1"/></linearGradient><clipPath id="round"><rect width="73.5" height="20" rx="3" fill="#fff"/></clipPath><g clip-path="url(#round)"><rect width="49.5" height="20" fill="#010000"/><rect x="49.5" width="24.0" height="20" fill="#01f000"/><rect width="73.5" height="20" fill="url(#smooth)"/></g><g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="110"><image x="5" y="3" width="14" height="14" href="https://avatars.githubusercontent.com/u/9265326?s=120&amp;v=4"/><text x="342.5" y="150" fill="#010101" fill-opacity=".3" transform="scale(0.1)" textLength="225.0" lengthAdjust="spacing">SSG</text><text x="342.5" y="140" transform="scale(0.1)" textLength="225.0" lengthAdjust="spacing">SSG</text><text x="605.0" y="150" fill="#010101" fill-opacity=".3" transform="scale(0.1)" textLength="140.0" lengthAdjust="spacing">36</text><text x="605.0" y="140" transform="scale(0.1)" textLength="140.0" lengthAdjust="spacing">36</text><a href="https://github.com/epogrebnyak"><rect width="49.5" height="20" fill="rgba(0,0,0,0)"/></a><a href="https://github.com/epogrebnyak"><rect x="49.5" width="24.0" height="20" fill="rgba(0,0,0,0)"/></a></g></svg>"""
    svg = badge_generate(
        left_text = 'SSG',
        right_text = '36',
        link = 'https://github.com/epogrebnyak',
        logo = 'https://avatars.githubusercontent.com/u/9265326?s=120&v=4',
        left_color = '#010000',
        right_color = '#01f000',
    )
    assert correct_svg == svg

