import socket
import threading

from src.data_saver.secured_data_saver import SecuredDataSaver
from src.small_conn.server_client.server_client_connection import ServerClientConnection
from src.small_conn.server_client.server_client_data_saver import ServerClientDataSaver
from src.utils.utils import find_changes_between_lists


class ServerConnection:

    def __init__(self, server_socket, addr, user_list):
        self.__server_connection = server_socket
        self.__server_connection.settimeout(2)
        self.__user_list: SecuredDataSaver = user_list
        self.__user_conn_list: SecuredDataSaver = SecuredDataSaver()
        self.__addr = addr
        self.__run = True
        threading.Thread(target=self.data_saver_update).start()

    def __connect_clients(self):
        try:
            server_client_socket, addr = self.__server_connection.accept()
        except socket.timeout:
            pass
        except OSError:
            pass
        else:
            pass
            server_client_connection = ServerClientConnection(server_client_socket, addr, ServerClientDataSaver())
            user_connection_thread = threading.Thread(target=self.user_connection, args=(server_client_connection,))
            user_connection_thread.start()

    def user_connection(self, server_client_connection):
        name = self.input_user_name(server_client_connection)
        if name:
            threading.Thread(target=self.disconnect_user_name, args=(name,)).start()

    def input_user_name(self, server_client_connection: ServerClientConnection):
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
            if self.__user_list.get_value(user_name[0]):
                server_client_connection.name_input_response("The name is all ready in use")
            else:
                server_client_connection.name_input_response("The name is not in use")
                server_client_connection.is_input_name = True
                self.__user_list.set_value(user_name[0], server_client_connection.get_server_client_data_saver())
                self.__user_conn_list.set_value(user_name[0], server_client_connection)
                print(f"[USER CONNECTED] {user_name[0]} {server_client_connection}")
                return user_name[0]

        server_client_connection.self_disconnect()

    def disconnect_user_name(self, name):
        server_client_connection: ServerClientConnection = self.__user_conn_list.get_value(name)
        while server_client_connection.is_handle_connection:
            if not self.__run:
                break

        server_client_connection.self_disconnect()
        self.__user_list.remove(name)
        self.__user_conn_list.remove(name)
        print(f"[USER DISCONNECTED] {name} {server_client_connection}")

    def remove_user_name(self, name):
        server_client_connection: ServerClientConnection = self.__user_conn_list.get_value(name)
        server_client_connection.self_disconnect()
        self.__user_list.remove(name)
        self.__user_conn_list.remove(name)
        print(f"[USER REMOVE] {name} {server_client_connection}")

    def disconnect_all_user_name(self):
        users_names = self.__user_list.get_keys()
        for _ in users_names:
            if self.__user_list.get_value(_):
                self.__user_list.remove(_)
                self.__user_conn_list.remove(_)

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
        self.disconnect_all_user_name()
        self.__server_connection.close()

    def data_saver_update(self):
        previous_users_names = []
        while self.__run:
            users_names = self.__user_list.get_keys()
            added, removed = find_changes_between_lists(previous_users_names, users_names)
            if len(removed) > 0:
                for _ in removed:
                    print("remove")
                    self.remove_user_name(_)

            previous_users_names = users_names
