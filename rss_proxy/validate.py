from rfc3986 import uri_reference


def url_validate(url: str) -> bool:
    u = uri_reference(url)
    if not u.is_valid(require_scheme=True,
                      require_authority=True,
                      require_path=True):
        return False

    return u.scheme in ['http', 'https']
