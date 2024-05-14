import threading

import cv2
import numpy as np
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

from src.share_screen_conn.server_client.screen_share_server_client_connection import ScreenShareServerClientConnection
from src.small_conn.server_client.server_client_data_saver import KeyValue


class Constance:
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 600
    NUMBER_OF_BYTES_PER_PIXEL = 3


class ScreenShareGui(QWidget):
    update_image_signal = pyqtSignal(QPixmap)

    def __init__(self, server_client_connection: ScreenShareServerClientConnection, name, users_with_share_screen_open,
                 user_data_saver):
        super().__init__()
        self.__server_client_connection = server_client_connection
        self.__users_with_share_screen_open = users_with_share_screen_open
        self.__user_data_saver = user_data_saver
        self.__name = name

        self.setWindowTitle(f"{name} share screen")
        self.resize(Constance.SCREEN_WIDTH, Constance.SCREEN_HEIGHT)
        self.setWindowIcon(QIcon(r'src/imgs/screen-removebg-preview.png'))

        self.__label = QLabel("Waiting for image...", self)
        self.__label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.__label)
        self.setLayout(layout)

        self.__run = True
        self.update_image_signal.connect(self.update_label)
        threading.Thread(target=self.update_img).start()

    @pyqtSlot(QPixmap)
    def update_label(self, pixmap):
        self.__label.setPixmap(pixmap.scaled(self.__label.size(), Qt.KeepAspectRatio))

    def update_img(self):
        while self.__run:
            img_data = self.__server_client_connection.get_image()
            if img_data:
                img_array = np.frombuffer(img_data, dtype=np.uint8)
                image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                height, width, channel = image.shape
                bytesPerLine = width * Constance.NUMBER_OF_BYTES_PER_PIXEL
                qt_image = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_image)
                self.update_image_signal.emit(pixmap)

    def stop(self):
        # it goes to the closeEvent before closing
        self.__run = False
        self.close()

    def closeEvent(self, event):
        self.__user_data_saver.set_value(KeyValue.IS_SERVER_SHARE_SCREEN, False)
