import threading

from src.connection.protocol import PacketType
from src.connection.single_connection import SocketConnection
from src.keys import key_inserter
from src.small_conn.client.client_data_saver import ClientDataSaver, KeyValue


class ClientServerConnection(SocketConnection):
    def __init__(self, client_socket, addr, client_data_saver: ClientDataSaver):
        super().__init__(client_socket, addr)
        self.start_handle_data()
        self.__client_data_saver = client_data_saver
        self.__name_input_feedback = ["", 0]
        self.is_input_name = False
        threading.Thread(target=self.data_saver_update).start()

    def _handle_data(self, packet_type, data):
        super()._handle_data(packet_type, data)
        if PacketType(packet_type) == PacketType.TEXT:
            print(data)

        if not self.is_input_name:
            if PacketType(packet_type) == PacketType.NAME_INPUT:
                self.__name_input_feedback[0] = data
                self.__name_input_feedback[1] += 1

        if PacketType(packet_type) == PacketType.KEYBOARD_KEY:
            key_inserter.send_key(data)

    def name_input_request(self, user_name):
        self.send_data(PacketType.NAME_INPUT, {"user name": user_name})

    def get_name_input_feedback(self):
        return self.__name_input_feedback

    def data_saver_update(self):
        prev_keyboard = False
        prev_share_Screen = False
        while self.is_handle_connection:
            current_keyboard = self.__client_data_saver.get_value(KeyValue.IS_CLIENT_KEYBOARD)
            current_share_Screen = self.__client_data_saver.get_value(KeyValue.IS_CLIENT_SHARE_SCREEN)

            if prev_keyboard != current_keyboard:
                self.send_data(PacketType.DATA_SAVER_UPDATE, (KeyValue.IS_CLIENT_KEYBOARD, current_keyboard))
                prev_keyboard = current_keyboard

            if prev_share_Screen != current_share_Screen:
                self.send_data(PacketType.DATA_SAVER_UPDATE, (KeyValue.IS_CLIENT_SHARE_SCREEN, current_share_Screen))
                prev_share_Screen = current_share_Screen
