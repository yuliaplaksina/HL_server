import os
import socket
from multiprocessing import Process

from Config import Config
from Worker import Worker


class Server(object):
    def __init__(self, config_path: str):
        self.__config = Config.set(config_path)

    def server_init(self):
        self.__socket_init()
        self.__workers_init()
        print(f'Server is running: \n address: http://{self.__config.address}:{self.__config.port}')

        self.__server_init()

    def __socket_init(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.__config.address, self.__config.port))
        server_socket.listen(512)

        self.__socket = server_socket

    def __workers_init(self):
        self.__processes = []

        for i in range(self.__config.cpu_limit):
            worker = Worker(self.__socket, self.__config)

            process = Process(
                target=worker.run
            )
            self.__processes.append(process)
            process.start()

    def __server_init(self):
        try:
            os.wait()
        except KeyboardInterrupt:
            for process in self.__processes:
                process.terminate()
            self.__socket.close()
