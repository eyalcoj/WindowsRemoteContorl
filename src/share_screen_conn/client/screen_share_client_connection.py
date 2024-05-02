from src.connection.protocol import PacketType
from src.connection.single_connection import SocketConnection


class ScreenShareClientServerConnection(SocketConnection):
    def __init__(self, client_socket, addr):
        super().__init__(client_socket, addr)
        self.__is_passing_share_screen = False

    def _handle_data(self, packet_type, data):
        super()._handle_data(packet_type, data)
        if PacketType(packet_type) == PacketType.SHARE_SCREEN_REQUEST:
            if data == "connect":
                self.__is_passing_share_screen = True
            elif data == "disconnect":
                self.__is_passing_share_screen = False

    def send_screen_share_frame(self, img_data):
        self.send_data(PacketType.IMG, img_data)

    def send_name(self, name):
        self.send_data(name, PacketType.NAME_INPUT)

    def is_passing_share_screen(self):
        return self.__is_passing_share_screen


