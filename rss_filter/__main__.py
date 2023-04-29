import cgi
from typing import Union
import chardet
import fastapi
import fake_useragent
import httpx

app = fastapi.FastAPI()

fake_ua = fake_useragent.UserAgent()

DEFAULT_TIMEOUT = httpx.Timeout(
    timeout=120,
    connect=5,
    read=120,
    write=120,
)


def get_ua(ua: str) -> str:
    if ua is None or ua == '' or ua.lower() == 'chrome':
        return fake_ua.chrome
    elif ua.lower() == 'firefox':
        return fake_ua.firefox
    elif ua.lower() == 'edge':
        return fake_ua.firefox
    elif ua.lower() == 'random':
        return fake_ua.random
    else:
        return ua


@app.get("/filter")
def filter(
    insecure: Union[bool, None] = fastapi.Query(default=False),
    ua: str = fastapi.Query(
        default='chrome',
        max_length=512,
    ),
    url: str = fastapi.Query(
        # https://uibakery.io/regex-library/url-regex-python
        regex='^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$',
        max_length=4096,
    ),
    encoding_in: str = fastapi.Query(
        default='auto',
        alias='encoding.in',
        max_length=64,
    ),
    channel_title: Union[str, None] = fastapi.Query(
        default=None,
        alias='channel.title',
    ),
    channel_link: Union[str, None] = fastapi.Query(
        default=None,
        alias='channel.link',
    ),
    channel_description: Union[str, None] = fastapi.Query(
        default=None,
        alias='channel.description',
    ),
    item_title: Union[str, None] = fastapi.Query(
        default=None,
        alias='item.title',
    ),
    item_link: Union[str, None] = fastapi.Query(
        default=None,
        alias='item.link',
    ),
    item_description: Union[str, None] = fastapi.Query(
        default=None,
        alias='item.description',
    ),
):

    # TODO uvicorn disable headers[server, date]
    # TODO error handling
    # TODO design query parameters
    # TODO verify parameters
    # TODO prevent gzip bomb (limit content read length)
    r = httpx.get(
        url=url,
        headers={'user-agent': get_ua(ua)},
        verify=not insecure,
        follow_redirects=True,
        timeout=DEFAULT_TIMEOUT,
    )

    if not httpx.codes.is_success(r.status_code):
        # TODO response for error
        return fastapi.Response(
            status_code=r.status_code
        )

    # TODO encoding
    if encoding_in == 'auto':
        charset = chardet.detect(r.content)
        encoding_in = charset.get('encoding')
        if encoding_in is None or encoding_in == '':
            encoding_in = 'utf-8'

    # TODO better way for cloning headers
    if r.headers.__contains__('content-encoding'):
        r.headers.__delitem__('content-encoding')
    if r.headers.__contains__('content-length'):
        r.headers.__delitem__('content-length')

    content = r.content.decode(encoding_in).encode()

    # TODO parse and generate rss (xml)
    # TODO format in/out

    content_type = 'text/html; charset=utf-8'
    if r.headers.get('content-type') is not None:
        content_type_full, content_type_params = cgi.parse_header(
            r.headers.get('content-type'),
        )
        if content_type_full is None or content_type_full == '':
            content_type_full = 'text/html'
        content_type_params = {'charset': 'utf-8'}
        content_type = content_type_full + '; ' + \
            "; ".join("=".join(_) for _ in content_type_params.items())

    r.headers['content-type'] = content_type

    # TODO response minify
    # TODO response gzip
    rr = fastapi.Response(
        content=content,
        status_code=r.status_code,
        headers=r.headers,
    )

    return rr
