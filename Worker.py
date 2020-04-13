from socket import socket

from Config import Config
from Request import Request
from Responder import Responder


class Worker(object):
    def __init__(self, sock: socket, config: Config):
        self.__socket = sock
        self.__config = config

        self.__responder = Responder(config)

    def run(self):
        while True:
            conn, _ = self.__socket.accept()
            conn.settimeout(10.0)

            try:
                raw_request = conn.recv(1024)
                request = Request(raw_request.decode('utf-8'))
                response = self.__responder.make_response(request)
                response.send(conn)
            except:
                pass
            finally:
                conn.close()
