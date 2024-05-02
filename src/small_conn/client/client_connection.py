from src.connection.protocol import PacketType
from src.connection.single_connection import SocketConnection


class ClientServerConnection(SocketConnection):
    def __init__(self, client_socket, addr):
        super().__init__(client_socket, addr)
        self.__name_input_feedback = ["", 0]
        self.is_input_name = False

    def _handle_data(self, packet_type, data):
        super()._handle_data(packet_type, data)
        if PacketType(packet_type) == PacketType.TEXT:
            print(data)
        if not self.is_input_name:
            if PacketType(packet_type) == PacketType.NAME_INPUT:
                self.__name_input_feedback[0] = data
                self.__name_input_feedback[1] += 1

    def name_input_request(self, user_name):
        self.send_data(PacketType.NAME_INPUT, {"user name": user_name})

    def get_name_input_feedback(self):
        return self.__name_input_feedback