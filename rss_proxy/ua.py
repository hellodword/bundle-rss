import fake_useragent


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
