"""Shared schema parsing helpers."""

import re
from html.parser import HTMLParser

from ..errors import ApiError

_RICH_CONTENT_TAG = re.compile(
    r"<\/?(?:p|div|h[1-6]|br|strong|b|em|i|ul|ol|li|table|thead|tbody|tr|th|td)\b",
    re.IGNORECASE,
)


class _TextContentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def plain_text(value: str) -> str:
    if not _RICH_CONTENT_TAG.search(value):
        return value
    parser = _TextContentParser()
    parser.feed(value)
    return "".join(parser.parts)


def parse_integer(value: object, label: str) -> int:
    try:
        if isinstance(value, bool):
            raise ValueError
        return int(value)
    except (TypeError, ValueError):
        raise ApiError(400, f"{label} must be an integer.") from None
