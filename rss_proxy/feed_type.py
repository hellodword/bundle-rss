from enum import IntEnum
from lxml import etree


class feedType(IntEnum):
    UNKNOWN = 0
    JSON = 1
    XML = 2
    ATOM = 4
    RSS = 8

    @classmethod
    def detect_content(cls, content: bytes) -> int:
        for ch in content:
            if ch in b' \n\r\t':
                continue
            elif ch in b'{':
                return cls.JSON
            elif ch in b'<':
                return cls.XML
            else:
                return cls.UNKNOWN

    @classmethod
    def detect_xml(cls, root) -> int:
        name = etree.QName(root)
        if name is None:
            return cls.UNKNOWN
        elif name.localname == 'feed':
            return cls.ATOM
        elif name.localname in ['rss', 'RDF']:
            return cls.RSS
        else:
            return cls.UNKNOWN
