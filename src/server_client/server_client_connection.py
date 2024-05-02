from src.connection.protocol import PacketType
from src.connection.single_connection import SingleConnection


class ServerClientConnection(SingleConnection):
    def __init__(self, server_client_socket, addr):
        super().__init__(server_client_socket, addr)
        self.__user_name = ["", 0]
        self.is_input_name = False

    def _handle_data(self, packet_type, data):
        print(packet_type)
        super()._handle_data(packet_type, data)
        if not self.is_input_name:
            if PacketType(packet_type) == PacketType.NAME_INPUT:
                self.__user_name[0] = data["user name"]
                self.__user_name[1] += 1
        if PacketType(packet_type) == PacketType.TEXT:
            print(data)

    def name_input_response(self, text):
        self.send_data(PacketType.NAME_INPUT, text)

    def get_user_name(self):
        return self.__user_name
