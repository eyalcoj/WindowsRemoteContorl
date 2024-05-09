import socket
import sys
import threading

from PyQt5.QtWidgets import QApplication

from src.data_saver.secured_data_saver import SecuredDataSaver
from src.keys.key_collector import KeyCollector
from src.share_screen_conn.server.server_connection import ShareScreenServerConnection
from src.small_conn.server.server_connection import ServerConnection
from src.small_conn.server.server_gui import ServerGui


class Constance:
    PORT = 8080
    # SERVER = socket.gethostbyname(socket.gethostname())
    SERVER = "0.0.0.0"
    ADDR = (SERVER, PORT)
    PORT_SHARE_SCREEN = 5050
    ADDR_SHARE_SCREEN = (SERVER, PORT_SHARE_SCREEN)


class ServerApplication:
    def __init__(self):
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__share_screen_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.__users_data_saver = SecuredDataSaver()
        self.__server_connection = ServerConnection(self.__server_socket, Constance.ADDR, self.__users_data_saver)
        self.__share_screen_server_connection = ShareScreenServerConnection(self.__share_screen_server_socket,
                                                                            Constance.ADDR_SHARE_SCREEN,
                                                                            self.__users_data_saver)
        self.__start()

        app = QApplication(sys.argv)


        self.server_gui = ServerGui(self.__users_data_saver, self.__share_screen_server_connection.get_users_conn())
        self.server_gui.show()
        app.exec_()

        self.__close()

    def __close(self):
        self.__server_connection.close_server()
        self.__share_screen_server_connection.close_server()

    def __start(self):
        self.__server_connection.connect()
        threading.Thread(target=self.__server_connection.start).start()
        self.__share_screen_server_connection.connect()
        threading.Thread(target=self.__share_screen_server_connection.start).start()
