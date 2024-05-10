import socket
import threading

import cv2
import numpy as np
import pyautogui

from src.share_screen_conn.client.screen_share_client_connection import ScreenShareClientServerConnection


class Constance:
    PORT = 8080
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)
    IMG_FORMAT = '.jpg'


class ShareScreenClientConnectionWraper:
    def __init__(self, share_screen_client_connection: ScreenShareClientServerConnection):
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__share_screen_client_connection = share_screen_client_connection
        self.__sending_share_screen_thread = threading.Thread(target=self.send_frames)
        self.__is_run = None

    @staticmethod
    def frame_build():
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        retval, buffer = cv2.imencode(Constance.IMG_FORMAT, screenshot_np)
        img_bytes = buffer.tobytes()
        return img_bytes

    def send_frames(self):
        while self.__is_run:
            if self.__share_screen_client_connection.is_passing_share_screen():
                frame = self.frame_build()
                self.__share_screen_client_connection.send_screen_share_frame(frame)

    def open(self):
        self.__share_screen_client_connection.connect()
        self.__is_run = True
        self.__sending_share_screen_thread.start()

    def close(self):
        self.__is_run = False
        self.__share_screen_client_connection.self_disconnect()
