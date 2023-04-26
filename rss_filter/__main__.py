from typing import Union
import fastapi
import fake_useragent
import httpx

app = fastapi.FastAPI()

fake_ua = fake_useragent.UserAgent()


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
    ua: Union[str, None] = fastapi.Query(default='chrome'),
    url: str = fastapi.Query(),
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

    r = httpx.get(
        url=url,
        headers={'user-agent': get_ua(ua)},
        verify=not insecure,
    )

    # TODO design query parameters
    # TODO parse xml
    # TODO encoding in/out
    # TODO format in/out
    # TODO uvicorn disable headers[server, date]

    return fastapi.Response(
        content=r.content,
        status_code=r.status_code,
        headers=r.headers,
    )
