from os import path
from enum import IntEnum

from Request import Request
from Response import Response
from Config import Config

ALLOWED_METHODS = {
    "GET",
    "HEAD"
}


class HTTPStatus(IntEnum):
    OK = 200
    Forbidden = 403
    NotFound = 404
    MethodNotAllowed = 405


HTTP_STATUS_MESSAGES = {
    HTTPStatus.OK: 'OK',
    HTTPStatus.Forbidden: 'Forbidden',
    HTTPStatus.NotFound: 'Not Found',
    HTTPStatus.MethodNotAllowed: 'Method Not Allowed'
}

class Responder(object):
    def __init__(self, config: Config):
        self.__config = config

    def make_response(self, request: Request):
        if request.method not in ALLOWED_METHODS:
            return Response(status=HTTPStatus.MethodNotAllowed)

        if '/../' in request.url:
            return Response(status=HTTPStatus.Forbidden)

        filepath = path.join(self.__config.document_root, request.url.lstrip('/'))
        if path.isdir(filepath):
            filepath = path.join(filepath, 'index.html')
            if not path.exists(filepath):
                return Response(status=HTTPStatus.Forbidden)

        if not path.isfile(filepath):
            return Response(status=HTTPStatus.NotFound)

        return Response(status=HTTPStatus.OK, method=request.method, protocol=request.protocol, filepath=filepath)
