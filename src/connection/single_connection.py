import threading
from abc import ABC, abstractmethod

from src.connection import protocol
from src.connection.protocol import PacketType


class SocketConnection(ABC):
    def __init__(self, socket, addr):
        self._socket = socket
        self._addr = addr
        self._handle_connection_thread = threading.Thread(target=self._handle_connection)
        self.is_handle_connection = False
        self.encryption_key = None

    def receive_data(self):
        if self.encryption_key:
            recv = protocol.recv2(self._socket, self.encryption_key)
        else:
            recv = protocol.recv2(self._socket)
        packet_type, data = recv
        if packet_type != PacketType.ERROR:
            if packet_type != PacketType.IMG:
                print(f"[RECEIVE_DATA] receive from {self._addr}: {(packet_type, data)}")
        return packet_type, data

    def send_data(self, packet_type: PacketType, data, is_bytes=False):
        if self.encryption_key:
            protocol.send2(packet_type, data, self._socket, is_bytes, encryption_key=self.encryption_key)
        else:
            protocol.send2(packet_type, data, self._socket, is_bytes)
        print(f"[SEND_DATA] send to {self._addr}: {packet_type, data}")

    def _handle_connection(self):
        print(f"\n[NEW CONNECTION] {self._addr} connected.")
        while self.is_handle_connection:
            packet_type, data = self.receive_data()
            if packet_type != PacketType.ERROR:
                self._handle_data(packet_type, data)

    def start_handle_data(self):
        self.is_handle_connection = True
        self._handle_connection_thread.start()

    def _stop_handle_data(self):
        self.is_handle_connection = False

    @abstractmethod
    def _handle_data(self, packet_type, data):
        if packet_type == PacketType.DISCONNECT:
            self.other_disconnect()

    def connect(self):
        print(f"[CONNECT] {self._addr}")
        self._socket.connect(self._addr)

    def self_disconnect(self):
        print(f"[SELF DISCONNECT] {self._addr}")
        self.send_data(PacketType.DISCONNECT, "")
        self._stop_handle_data()

    def other_disconnect(self):
        print(f"[OTHER DISCONNECT] {self._addr}")
        self._stop_handle_data()
        self._socket.close()
