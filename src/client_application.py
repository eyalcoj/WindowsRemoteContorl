import socket

from src.share_screen_conn.client.screen_share_client_connection import ScreenShareClientServerConnection
from src.share_screen_conn.client.share_screen_client_connection_wraper import ShareScreenClientConnectionWraper
from src.small_conn.client.client_connection import ClientServerConnection


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
        self.feedback_number = 0
        self.feedback = ""

        self.__client_connection = ClientServerConnection(self.__client_socket, Constance.ADDR)
        self.__share_screen_client_connection = ScreenShareClientServerConnection(self.__client_socket, Constance.ADDR)
        self.share_screen_client_connection_wraper = ShareScreenClientConnectionWraper(
            self.__share_screen_client_connection)

        self.__start()

        self.input_user_name(input("enter you name: "))

        print(self.feedback)

        input("enter somthing\n")

        self.__close()

    def input_user_name(self, name):
        self.__client_connection.name_input_request(name)

        feedback = self.__client_connection.get_name_input_feedback()
        while self.feedback_number == feedback[1]:
            feedback = self.__client_connection.get_name_input_feedback()

        self.feedback_number == feedback[1]
        self.feedback = feedback[0]

    def __close(self):
        self.__client_connection.self_disconnect()
        self.share_screen_client_connection_wraper.close()

    def __start(self):
        self.__client_connection.connect()
        self.share_screen_client_connection_wraper.open()
