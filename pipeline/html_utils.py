import re

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text


__all__ = [
    'minify_html_leave_whitespace'
]


def minify_html_leave_whitespace(value):
    """
    Custom minify_html function which leaves one empty space between HTML tags.
    """
    value = re.sub(r'\r\n', ' ', force_text(value))
    value = re.sub(r'\n', ' ', value)
    value = re.sub(r'>\s+<', '> <', value)
    return value
