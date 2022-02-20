import hashlib


def shortit(long_url: str) -> str:
    return hashlib.sha1(long_url.encode("UTF-8")).hexdigest()[:8]
