import threading
import time

from src.connection.protocol import PacketType
from src.data_saver.secured_data_saver import SecuredDataSaver
from src.server_client.server_client_connection import ServerClientConnection
from src.server_client.server_client_data_saver import ServerClientDataSaver


class ServerConnection:

    def __init__(self, server_socket, addr, user_list):
        self.__server_connection = server_socket
        self.__user_list: SecuredDataSaver = user_list
        self.__user_conn_list: SecuredDataSaver = SecuredDataSaver()
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
            user_connection_thread = threading.Thread(target=self.user_connection, args=(server_client_connection, ))
            user_connection_thread.start()

    def user_connection(self, server_client_connection):
        name = self.input_user_name_logic(server_client_connection)
        if name:
            self.disconnect_user_name_logic(name)

    def input_user_name_logic(self, server_client_connection: ServerClientConnection):
        user_name_number = 0
        while not server_client_connection.is_input_name:
            if not self.__run:
                break
            user_name = server_client_connection.get_user_name()
            while user_name_number == user_name[1]:
                user_name = server_client_connection.get_user_name()
                if not self.__run:
                    break
            user_name_number = user_name[1]

            if not self.__run:
                break
            if user_name[0] in self.__user_list:
                server_client_connection.name_input_response("The name is all ready in use")
            else:
                server_client_connection.name_input_response("The name is not in use")
                server_client_connection.is_input_name = True
                self.__user_list.set_value(user_name[0], ServerClientDataSaver())
                self.__user_conn_list.set_value(user_name[0], server_client_connection)
                print(f"[USER CONNECTED] {user_name[0]} {server_client_connection}")
                return user_name[0]

    def disconnect_user_name_logic(self, name):
        server_client_connection: ServerClientConnection = self.__user_conn_list.get_value(name)
        while server_client_connection.is_handle_connection:
            if not self.__run:
                break
        self.__user_list.remove(name)
        print(f"[USER DISCONNECTED] {name} {server_client_connection}")
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
