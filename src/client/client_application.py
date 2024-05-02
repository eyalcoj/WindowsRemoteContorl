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
        self.__run = True
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.feedback_number = 0
        self.feedback = ""

        self.__client_connection = ClientServerConnection(self.__client_socket, Constance.ADDR)
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

    def __start(self):
        self.__client_connection.connect()
