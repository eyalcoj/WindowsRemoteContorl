import socket
import sys
import threading

from PyQt5.QtWidgets import QApplication

from src.share_screen_conn.client.screen_share_client_connection import ScreenShareClientServerConnection
from src.share_screen_conn.client.share_screen_client_connection_wraper import ShareScreenClientConnectionWraper
from src.small_conn.client.client_connection import ClientServerConnection
from src.small_conn.client.client_connection_warper import ClientConnectionWarper
from src.small_conn.client.client_data_saver import ClientDataSaver
from src.small_conn.client.gui.client_gui import ClientUserGui
from src.small_conn.client.gui.client_name_input_gui import NameInputGUI


class Constance:
    PORT = 8080
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)
    PORT_SHARE_SCREEN = 5050
    ADDR_SHARE_SCREEN = (SERVER, PORT_SHARE_SCREEN)


class ClientApplication:
    def __init__(self):
        self.__run = True
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__share_screen_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client_data_saver = ClientDataSaver()

        self.feedback_number = 0
        self.feedback = ""

        self.__client_connection = ClientServerConnection(self.__client_socket, Constance.ADDR, self.__client_data_saver)
        self.__client_connection_warper = ClientConnectionWarper(self.__client_connection)

        self.__share_screen_client_connection = ScreenShareClientServerConnection(self.__share_screen_client_socket,
                                                                                  Constance.ADDR_SHARE_SCREEN,
                                                                                  self.__client_data_saver)
        self.__share_screen_client_connection_wraper = ShareScreenClientConnectionWraper(
            self.__share_screen_client_connection)

        self.t1 = None
        self.t2 = None

        self.__client_connection_warper.open()
        self.__share_screen_client_connection_wraper.open()

        app = QApplication(sys.argv)
        print("dgsdsgdg")
        self.name_input_gui = NameInputGUI(self.__client_connection_warper)
        self.name_input_gui.show()
        self.t1 = threading.Thread(target=self.check_conn, args=(self.name_input_gui,))
        self.t1.start()

        app.exec_()

        user_name = self.name_input_gui.get_name()
        if user_name != "":
            self.__share_screen_client_connection.send_name(user_name)
            self.client_user_gui = ClientUserGui(user_name, self.__client_data_saver)
            self.client_user_gui.show()
            self.t2 = threading.Thread(target=self.check_conn, args=(self.client_user_gui,))
            self.t2.start()
            app.exec_()
        else:
            self.__share_screen_client_connection.send_name("haha")





        self.__close()

    def check_conn(self, gui):
        while self.__client_connection.is_handle_connection:
            if not self.__run:
                break
        gui.close()

    def __close(self):
        self.__client_connection_warper.close()
        self.__share_screen_client_connection_wraper.close()
        self.__run = False

        if self.t1.is_alive():
            self.t1.join()

        if self.t2 and self.t2.is_alive():
            self.t2.join()

        sys.exit()

    # def __start(self):
    #     self.__client_connection_warper.open()
    #     self.__share_screen_client_connection_wraper.open()
