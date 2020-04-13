from urllib import parse


class Request(object):
    def __init__(self, raw: str):
        self.__parse(raw)

    def __parse(self, raw: str):
        strings = raw.split('\r\n')
        try:
            method, url, protocol = strings[0].split(' ')

            self.method = method
            self.protocol = protocol

            url = parse.unquote(url)
            if '?' in url:
                url = url[:url.index('?')]

            self.url = url
        except Exception:
            pass
