import socket
import time

from src.server.server_connection import ServerConnection


class Constance:
    PORT = 8080
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)


class ServerApplication:
    def __init__(self):
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.__server_connection = ServerConnection(self.__server_socket, Constance.ADDR, [])
        self.__start()

    def __close(self):
        self.__server_connection.close_server()

    def __start(self):
        self.__server_connection.connect()
        self.__server_connection.start()
