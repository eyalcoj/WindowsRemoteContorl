from src.connection.protocol import PacketType
from src.connection.single_connection import SingleConnection


class ClientServerConnection(SingleConnection):
    def __init__(self, client_socket, addr):
        super().__init__(client_socket, addr)

    def _handle_data(self, packet_type, data):
        super()._handle_data(packet_type, data)
        if PacketType(packet_type) == PacketType.TEXT:
            print(data)


class ClientServerConnectionLogin(SingleConnection):
    def __init__(self, client_socket, addr):
        super().__init__(client_socket, addr)
        self.login_feedback = ""
        self.register_feedback = ""

    def _handle_data(self, packet_type, data):
        super()._handle_data(packet_type, data)
        if PacketType(packet_type) == PacketType.LOGIN:
            self.login_feedback = data
        if PacketType(packet_type) == PacketType.REGISTER:
            self.register_feedback = data

    def login_logic(self, user_name, password):
        self.send_data(PacketType.LOGIN, {"user name": user_name, "password": password})

    def register_logic(self, user_name, password):
        self.send_data(PacketType.REGISTER, {"user name": user_name, "password": password})
