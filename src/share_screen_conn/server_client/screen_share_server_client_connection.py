from src.connection.protocol import PacketType
from src.connection.single_connection import SocketConnection


class ScreenShareServerClientConnection(SocketConnection):
    def __init__(self, server_client_socket, addr):
        super().__init__(server_client_socket, addr)
        self.__image = 0

    def _handle_data(self, packet_type, data):
        super()._handle_data(packet_type, data)
        if PacketType.IMG == PacketType(packet_type):
            self.__image = data

    def get_image(self):
        return self.__image

    def send_connect_request(self):
        self.send_data(PacketType.SHARE_SCREEN_REQUEST, "connect")

    def send_disconnect_request(self):
        self.send_data(PacketType.SHARE_SCREEN_REQUEST, "disconnect")
