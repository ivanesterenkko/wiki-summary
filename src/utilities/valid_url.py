from urllib.parse import urlparse

def is_valid_wiki_url(url: str) -> bool:
    parts = urlparse(url)
    return (
        parts.scheme in ("http", "https")
        and "wikipedia.org" in parts.netloc
        and parts.path.startswith("/wiki/")
    )