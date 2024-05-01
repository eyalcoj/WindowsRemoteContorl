import threading
from abc import ABC, abstractmethod

from src.connection import protocol
from src.connection.protocol import PacketType


class SingleConnection(ABC):
    def __init__(self, socket, addr):
        self._socket = socket
        self._addr = addr
        self._handle_connection_thread = threading.Thread(target=self._handle_connection)
        self._is_handle_connection = None
        self._start_handle_data()

    def _receive_data(self):
        packet_type, data = protocol.recv2(self._socket)
        if packet_type != PacketType.ERROR:
            print(f"[RECEIVE_DATA] receive from {self._addr}: {(packet_type, data)}")
        return packet_type, data

    def send_data(self, packet_type: PacketType, data):
        protocol.send2(packet_type, data, self._socket)
        print(f"[SEND_DATA] send to {self._addr}: {packet_type, data}")

    def _handle_connection(self):
        print(f"\n[NEW CONNECTION] {self._addr} connected.")
        while self._is_handle_connection:
            packet_type, data = self._receive_data()
            if packet_type != PacketType.ERROR:
                self._handle_data(packet_type, data)

    def _start_handle_data(self):
        self._is_handle_connection = True
        self._handle_connection_thread.start()

    def _stop_handle_data(self):
        self._is_handle_connection = False

    @abstractmethod
    def _handle_data(self, packet_type, data):
        if packet_type == PacketType.DISCONNECT:
            self._other_disconnect()

    def connect(self):
        print(f"[CONNECT] {self._addr}")
        self._socket.connect(self._addr)

    def self_disconnect(self):
        print(f"[SELF DISCONNECT] {self._addr}")
        self.send_data(PacketType.DISCONNECT, "")
        self._stop_handle_data()

    def _other_disconnect(self):
        print(f"[OTHER DISCONNECT] {self._addr}")
        self._stop_handle_data()
        self._socket.close()
