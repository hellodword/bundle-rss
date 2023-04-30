from io import BytesIO
from lxml import etree
import cgi
from typing import Union
from enum import Enum
import chardet
import fastapi
import httpx
from fastapi.middleware.gzip import GZipMiddleware
from rss_proxy.feed_type import feedType
from rss_proxy.ua import get_ua
from rss_proxy.validate import url_validate


DEFAULT_TIMEOUT = httpx.Timeout(
    timeout=120,
    connect=5,
    read=120,
    write=120,
)


class FormatEnum(str, Enum):
    RSS = "rss"
    ATOM = "atom"
    JSON = "json"


app = fastapi.FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.get('/proxy')
def proxy(
    insecure: Union[bool, None] = fastapi.Query(default=False),
    ua: str = fastapi.Query(
        default='chrome',
        max_length=512,
    ),
    url: str = fastapi.Query(
        max_length=4096,
    ),
    in_encoding: str = fastapi.Query(
        default='auto',
        alias='in.encoding',
        max_length=64,
    ),
    out_format: Union[FormatEnum, None] = fastapi.Query(
        default=FormatEnum.RSS,
        alias='out.format',
    ),
    pretty: Union[bool, None] = fastapi.Query(default=True),
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

    # TODO design query parameters
    # TODO verify parameters

    if not url_validate(url):
        return fastapi.Response(
            status_code=httpx.codes.BAD_REQUEST
        )

    try:
        raw_content = BytesIO()
        with httpx.stream(
            method='GET',
            url=url,
            headers={'user-agent': get_ua(ua)},
            # TODO ja3
            verify=not insecure,
            follow_redirects=True,
            timeout=DEFAULT_TIMEOUT,
        ) as r:
            # TODO allow non-2xx response
            if not httpx.codes.is_success(r.status_code):
                print(f'{r.status_code}')
                # TODO response for error
                return fastapi.Response(
                    status_code=r.status_code
                )
            status_code = r.status_code
            headers = r.headers
            l = 0
            for data in r.iter_bytes():
                l += len(data)
                # prevent gzip bomb (limit content read length)
                if l >= 1024*1024*4:  # 4MB
                    return fastapi.Response(
                        status_code=httpx.codes.INTERNAL_SERVER_ERROR
                    )
                raw_content.write(data)

    except Exception as e:
        print(f'{e=}')
        return fastapi.Response(
            status_code=httpx.codes.INTERNAL_SERVER_ERROR
        )

    try:
        if in_encoding == 'auto':
            charset = chardet.detect(raw_content.getvalue())
            in_encoding = charset.get('encoding')
            if in_encoding is None or in_encoding == '':
                in_encoding = 'utf-8'
        content = raw_content.getvalue().decode(in_encoding).encode()
    except Exception as e:
        print(f'{e=}')
        return fastapi.Response(
            status_code=httpx.codes.INTERNAL_SERVER_ERROR
        )

    # TODO parse and generate rss (xml)

    content_type_fulls = {
        FormatEnum.ATOM: 'application/xml',
        FormatEnum.RSS: 'application/xml',
        FormatEnum.JSON: 'application/json',
    }

    content_type_full = content_type_fulls[out_format]
    content_type_params = {'charset':  'utf-8'}

    feed_type = feedType.detect_content(content)
    print(f'{feed_type=}')
    if feed_type == feedType.JSON:
        # TODO json
        return fastapi.Response(
            status_code=httpx.codes.INTERNAL_SERVER_ERROR,
        )
    elif feed_type == feedType.XML:
        try:
            root = etree.XML(content)
        except etree.XMLSyntaxError as e:
            return fastapi.Response(
                status_code=httpx.codes.INTERNAL_SERVER_ERROR,
            )

        feed_type = feedType.detect_xml(root)
        print(f'{feed_type=}')
        if feed_type == feedType.ATOM:
            # TODO atom
            pass
        elif feed_type == feedType.RSS:
            # TODO rss
            pass
        else:
            return fastapi.Response(
                status_code=httpx.codes.INTERNAL_SERVER_ERROR,
            )
    else:
        return fastapi.Response(
            status_code=httpx.codes.INTERNAL_SERVER_ERROR,
        )

    # TODO filter items
    # TODO generate new rss (json/atom/rss)

    output_content = etree.tostring(root, pretty_print=pretty)

    content_type = content_type_full + '; ' + \
        '; '.join('='.join(_) for _ in content_type_params.items())

    rr = fastapi.Response(
        content=output_content,
        status_code=status_code,
        headers={'content-type': content_type},
    )

    return rr
