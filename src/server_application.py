import socket
import threading

from src.data_saver.secured_data_saver import SecuredDataSaver
from src.application.server.server_connection import ServerConnection
from src.share_screen.server.server_connection import ShareScreenServerConnection


class Constance:
    PORT = 8080
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)
    PORT_SHARE_SCREEN = 5050
    ADDR_SHARE_SCREEN = (SERVER, PORT_SHARE_SCREEN)


class ServerApplication:
    def __init__(self):
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__users_data_saver = SecuredDataSaver()
        self.__server_connection = ServerConnection(self.__server_socket, Constance.ADDR, self.__users_data_saver)
        self.__share_screen_server_connection = ShareScreenServerConnection(self.__server_socket,
                                                                            Constance.ADDR_SHARE_SCREEN,
                                                                            self.__users_data_saver)
        threading.Thread(target=self.__start).start()

        input("enter somthing\n")

        self.__close()

    def __close(self):
        self.__server_connection.close_server()
        self.__share_screen_server_connection.close_server()

    def __start(self):
        self.__server_connection.connect()
        self.__server_connection.start()
        self.__share_screen_server_connection.connect()
        self.__share_screen_server_connection.start()
