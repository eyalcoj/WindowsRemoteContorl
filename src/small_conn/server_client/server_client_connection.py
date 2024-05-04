from src.connection.protocol import PacketType
from src.connection.single_connection import SocketConnection
from src.small_conn.server_client.server_client_data_saver import ServerClientDataSaver


class ServerClientConnection(SocketConnection):
    def __init__(self, server_client_socket, addr, server_client_data_saver: ServerClientDataSaver):
        super().__init__(server_client_socket, addr)
        self.start_handle_data()
        self.__server_client_data_saver = server_client_data_saver
        self.__user_name = ["", 0]
        self.is_input_name = False

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

    def name_input_response(self, text):
        self.send_data(PacketType.NAME_INPUT, text)

    def get_user_name(self):
        return self.__user_name

    def get_server_client_data_saver(self):
        return self.__server_client_data_saver
