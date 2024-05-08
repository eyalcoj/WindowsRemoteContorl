import socket
import threading

from src.data_saver.secured_data_saver import SecuredDataSaver
from src.share_screen_conn.server_client.screen_share_server_client_connection import ScreenShareServerClientConnection


class ShareScreenServerConnection:

    def __init__(self, server_socket, addr, user_list):
        self.__server_connection = server_socket
        self.__server_connection.settimeout(2)
        self.__addr = addr
        self.__user = user_list
        self.__users_conn_list = SecuredDataSaver()
        self.__run = True

    def __connect_clients(self):
        try:
            server_client_socket, addr = self.__server_connection.accept()
        except socket.timeout:
            pass
        except OSError:
            pass
        else:
            pass
            server_client_connection = ScreenShareServerClientConnection(server_client_socket, addr)
            user_connection_thread = threading.Thread(target=self.user_connection, args=(server_client_connection,))
            user_connection_thread.start()

    def user_connection(self, screen_share_client_connection: ScreenShareServerClientConnection):
        name = self.input_user_name(screen_share_client_connection)
        if name:
            screen_share_client_connection.start_handle_data()
            threading.Thread(target=self.disconnect_user_name, args=(name,)).start()

    def input_user_name(self, server_client_connection: ScreenShareServerClientConnection):
        user_name = server_client_connection.receive_data()[1]
        self.__users_conn_list.set_value(user_name, server_client_connection)
        print(f"[USER CONNECTED] {user_name} {server_client_connection}")
        return user_name

    def disconnect_user_name(self, name):
        server_client_connection: ScreenShareServerClientConnection = self.__users_conn_list.get_value(name)
        while server_client_connection.is_handle_connection:
            if not self.__run:
                break

        server_client_connection.self_disconnect()
        self.__users_conn_list.remove(name)
        print(f"[USER DISCONNECTED] {name} {server_client_connection}")

    def disconnect_all_user_name(self):
        users_names = self.__users_conn_list.get_keys()
        for _ in users_names:
            if self.__users_conn_list.get_value(_):
                self.__users_conn_list.remove(_)

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

    def get_users_conn(self):
        return self.__users_conn_list
