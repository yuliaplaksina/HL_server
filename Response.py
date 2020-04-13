import os
import mimetypes
from datetime import datetime
from socket import socket


class Response(object):
    def __init__(self, status: int, method: str = 'GET', protocol: str = 'HTTP/1.1', filepath: str = None):
        self.__status = status
        self.__method = method
        self.__protocol = protocol
        self.__set_base_headers()
        self.__filepath = filepath
        if filepath is not None:
            self.__set_mime_headers()

    def __set_base_headers(self):
        self.__headers = {
            'Connection': 'close',
            'Server': 'HL_server',
            'Date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
        }

    def __set_mime_headers(self):
        mime, _ = mimetypes.guess_type(self.__filepath)
        self.__headers['Content-Type'] = mime
        self.__headers['Content-Length'] = str(os.path.getsize(self.__filepath))

    def send(self, conn: socket):
        from Responder import HTTP_STATUS_MESSAGES

        headers = f'{self.__protocol} {self.__status} {HTTP_STATUS_MESSAGES[self.__status]}\r\n'
        headers += '\r\n'.join([f'{key}: {value}' for key, value in self.__headers.items()]) + '\r\n\r\n'

        conn.sendall(headers.encode('utf-8'))
        if self.__filepath is None or self.__method == 'HEAD':
            return

        with open(self.__filepath, 'rb') as file:
            conn.sendfile(file)
