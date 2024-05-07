import base64
import json
import socket
from enum import Enum
from Crypto.Cipher import DES


class Constants:
    HEADER = 10  # Increase header size if necessary
    FORMAT = 'utf-8'


class PacketType(Enum):
    ERROR = -1
    DISCONNECT = 0
    NAME_INPUT = 1
    REGISTER = 2
    LOGOUT = 3
    TEXT = 4
    IMG = 5
    SHARE_SCREEN_REQUEST = 6
    DATA_SAVER_UPDATE = 7
    KEYBOARD_KEY = 8
    ENCRYPTION_KEY = 9


def send2(packet_type: PacketType, payload, conn: socket.socket, is_bytes=False, encryption_key=None):
    try:
        if is_bytes:
            encoded_payload = base64.b64encode(payload).decode(Constants.FORMAT)  # Encode bytes to Base64 string
            packet_dict = {"type": packet_type.value, "data": encoded_payload, "is_bytes": True}
        else:
            packet_dict = {"type": packet_type.value, "data": payload, "is_bytes": False}

        packet_json = json.dumps(packet_dict)
        packet_length = len(packet_json)
        packet_length_encoded = str(packet_length).encode(Constants.FORMAT)
        packet_length_encoded += b' ' * (Constants.HEADER - len(packet_length_encoded))
        conn.sendall(packet_length_encoded)
        if encryption_key:
            cipher = DES.new(encryption_key, DES.MODE_ECB)
            encrypt_data = cipher.encrypt(packet_json.encode(Constants.FORMAT))
            conn.sendall(encrypt_data)
        else:
            conn.sendall(packet_json.encode(Constants.FORMAT))
    except Exception as e:
        print(f"[SEND2 ERROR]: {e}")


def recv2(conn: socket.socket, encryption_key=None):
    try:
        packet_length_encoded = conn.recv(Constants.HEADER)
        if packet_length_encoded:
            packet_length = int(packet_length_encoded.decode(Constants.FORMAT).strip())
            print("dgddfd")
            if encryption_key:
                cipher = DES.new(encryption_key, DES.MODE_ECB)
                packet_json = cipher.decrypt(conn.recv(packet_length))
                packet_json = packet_json.decode(Constants.FORMAT)
            else:
                packet_json = conn.recv(packet_length).decode(Constants.FORMAT)
            packet_dict = json.loads(packet_json)
            packet_type = PacketType(packet_dict["type"])
            data = packet_dict["data"]
            if packet_dict["is_bytes"]:
                data = base64.b64decode(data.encode(Constants.FORMAT))  # Decode Base64 back to bytes
            return packet_type, data
        else:
            return PacketType.ERROR, None
    except Exception as e:
        # print(f"[ERROR] in receive_packet: {e}")
        return PacketType.ERROR, None
