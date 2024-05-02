import json
import socket
from enum import Enum


class Constants:
    HEADER = 5
    FORMAT = 'utf-8'


class PacketType(Enum):
    ERROR = -1
    DISCONNECT = 0
    NAME_INPUT = 1
    REGISTER = 2
    LOGOUT = 3
    TEXT = 4



def __send_by_socket(payload: dict, conn: socket.socket(socket.AF_INET, socket.SOCK_STREAM)):
    try:
        if payload:
            payload_json = json.dumps(payload)
            payload_length = len(payload_json)
            encode_payload_length = str(payload_length).encode(Constants.FORMAT)
            encode_payload_length = b' ' * (Constants.HEADER - len(encode_payload_length)) + encode_payload_length
            conn.send(encode_payload_length + payload_json.encode(Constants.FORMAT))

    except Exception as e:
        print(f"[ERROR] in send_package: {e}")
        pass


def __receive_by_socket(conn: socket.socket(socket.AF_INET, socket.SOCK_STREAM)):
    try:
        organized_payload_length = conn.recv(Constants.HEADER)
        if organized_payload_length:
            organized_payload_length = int(organized_payload_length.decode(Constants.FORMAT))
            payload = conn.recv(organized_payload_length).decode(Constants.FORMAT)
            return payload

    except Exception as e:
        print(f"[ERROR] in recv_package: {e}")
        pass


def __wrap_packet(packet_type: PacketType, payload: str):
    packet_dict = {
        "type": packet_type.value,
        "data": payload
    }
    return packet_dict


def __extract_packet(payload: str):
    packet_dict = json.loads(payload)
    packet_type = packet_dict["type"]
    data = packet_dict["data"]
    return packet_type, data


def send2(packet_type: PacketType, payload: str, conn: socket.socket(socket.AF_INET, socket.SOCK_STREAM)):
    packet_dict = __wrap_packet(packet_type, payload)
    __send_by_socket(packet_dict, conn)


def recv2(conn: socket.socket(socket.AF_INET, socket.SOCK_STREAM)):
    packet_json = __receive_by_socket(conn)
    if packet_json:
        packet_type, data = __extract_packet(packet_json)
        return PacketType(packet_type), data
    else:
        return PacketType.ERROR, ""
