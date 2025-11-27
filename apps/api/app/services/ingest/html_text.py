from html import unescape
import re

TAG_RE = re.compile(r"<[^>]+>")


def html_to_text(html: str) -> str:
    text = TAG_RE.sub(" ", html)
    return unescape(re.sub(r"\s+", " ", text)).strip()
