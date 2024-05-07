import threading
import time

from diffiehellman.diffiehellman import DiffieHellman

from src.connection.protocol import PacketType
from src.connection.single_connection import SocketConnection
from src.keys.key_collector import KeyCollector
from src.small_conn.server_client.server_client_data_saver import ServerClientDataSaver, KeyValue


class ServerClientConnection(SocketConnection):
    def __init__(self, server_client_socket, addr, server_client_data_saver: ServerClientDataSaver):
        super().__init__(server_client_socket, addr)
        # server_dh = DiffieHellman()
        # server_dh.generate_public_key()
        # data = str(server_dh.public_key)
        # packet_length_encoded = str(len(data)).encode('utf-8')
        # packet_length_encoded += b' ' * (5 - len(data))
        # server_client_socket.sendall(packet_length_encoded)
        # server_client_socket.sendall(data.encode('utf-8'))
        # data_size = int(server_client_socket.recv(4).decode('utf-8'))
        # print(f"fsfgfdgfd{data_size}fdgdfg")
        # server_public_key = int(server_client_socket.recv(data_size).decode('utf-8'))
        # print(f"fgdfdgdf{server_public_key}")
        # print(f"fgdfdgdf{type(server_public_key)}")
        # self.encryption_key = server_dh.generate_shared_secret(server_public_key)

        self.start_handle_data()
        self.__server_client_data_saver = server_client_data_saver
        self.__user_name = ["", 0]
        self.is_input_name = False
        threading.Thread(target=self.data_saver_update).start()

    def _handle_data(self, packet_type, data):
        super()._handle_data(packet_type, data)
        if not self.is_input_name:
            if PacketType(packet_type) == PacketType.NAME_INPUT:
                self.__user_name[0] = data["user name"]
                self.__user_name[1] += 1
        if PacketType(packet_type) == PacketType.TEXT:
            print(data)
        if PacketType(packet_type) == PacketType.DATA_SAVER_UPDATE:
            self.__server_client_data_saver.set_value(data[0], data[1])

    def data_saver_update(self):
        is_state_listening_for_keys = False
        keyboard_keys: KeyCollector = self.__server_client_data_saver.get_value(KeyValue.KEY_COLLECTOR)

        while self.is_handle_connection:
            if self.__server_client_data_saver.get_value(
                    KeyValue.IS_SERVER_KEYBOARD) and self.__server_client_data_saver.get_value(
                    KeyValue.IS_CLIENT_KEYBOARD):
                if not is_state_listening_for_keys:
                    keyboard_keys.start_listening()
                    is_state_listening_for_keys = True
                q = keyboard_keys.get_queue()
                if not q.empty():
                    self.send_data(PacketType.KEYBOARD_KEY, keyboard_keys.get_queue().get())

            else:
                if is_state_listening_for_keys:
                    keyboard_keys.stop_listening()
                    is_state_listening_for_keys = False

    def name_input_response(self, text):
        self.send_data(PacketType.NAME_INPUT, text)

    def get_user_name(self):
        return self.__user_name

    def get_server_client_data_saver(self):
        return self.__server_client_data_saver
