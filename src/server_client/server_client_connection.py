from src.connection.protocol import PacketType
from src.connection.single_connection import SingleConnection


class ServerClientConnection(SingleConnection):
    def __init__(self, server_client_socket, addr):
        super().__init__(server_client_socket, addr)

    def _handle_data(self, packet_type, data):
        print(packet_type)
        super()._handle_data(packet_type, data)
        if PacketType(packet_type) == PacketType.TEXT:
            print(data)


class ServerClientConnectionLogin(SingleConnection):
    def __init__(self, client_socket, addr):
        super().__init__(client_socket, addr)

    def _handle_data(self, packet_type, data):
        super()._handle_data(packet_type, data)
        if PacketType(packet_type) == PacketType.LOGIN:
            login_user_name = data["user name"]
            login_password = data["password"]
        if PacketType(packet_type) == PacketType.REGISTER:
            register_user_name = data["user name"]
            register_password = data["password"]

    def login_logic(self, user_name, password):
        self.send_data(PacketType.LOGIN, {"user name": user_name, "password": password})
