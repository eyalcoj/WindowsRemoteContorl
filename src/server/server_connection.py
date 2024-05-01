import time

from src.connection.protocol import PacketType
from src.server_client.server_client_connection import ServerClientConnection


class ServerConnection:

    def __init__(self, server_socket, addr):
        self.__server_connection = server_socket
        self.__addr = addr
        self.__run = True

    def __connect_clients(self):
        try:
            server_client_socket, addr = self.__server_connection.accept()
        except OSError:
            pass
        else:
            pass
            server_client_connection = ServerClientConnection(server_client_socket, addr)

    def connect(self):
        print("[SERVER] connect")
        self.__server_connection.bind(self.__addr)
        self.__server_connection.listen()

    def start(self):
        print("[RUN] server is running")
        while self.__run:
            self.__connect_clients()

    def close_server(self):
        print("[SERVER] close")
        self.__run = False
        self.__server_connection.close()