from urllib.parse import urljoin

BASE = "https://api.transip.nl/v6/"


def build_url(path: str):
    if path.startswith("/"):
        raise ValueError("Path must be relative (remove the leading slash)")
    return urljoin(BASE, path)
