import socket
import time

from src.client.client_connection import ClientServerConnection
from src.connection.protocol import PacketType


class Constance:
    PORT = 8080
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)


class ClientApplication:
    def __init__(self):
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.__client_connection = ClientServerConnection(self.__client_socket, Constance.ADDR)
        self.__start()

    def __close(self):
        self.__client_connection.self_disconnect()

    def __start(self):
        self.__client_connection.connect()
