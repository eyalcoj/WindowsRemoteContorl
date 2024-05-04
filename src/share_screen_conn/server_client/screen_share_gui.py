import io
import threading
from PIL import Image
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

from src.share_screen_conn.server_client.screen_share_server_client_connection import ScreenShareServerClientConnection

class ScreenShareGui(QWidget):
    update_image_signal = pyqtSignal(QPixmap)  # Define a signal that carries a QPixmap object

    def __init__(self, server_client_connection: ScreenShareServerClientConnection, name, users_with_share_screen_open):
        super().__init__()
        self.__server_client_connection = server_client_connection
        self.__users_with_share_screen_open = users_with_share_screen_open
        self.__name = name

        self.setWindowTitle(name)
        self.__label = QLabel("Waiting for image...", self)
        self.__label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.__label)
        self.setLayout(layout)

        self.__run = True
        self.update_image_signal.connect(self.update_label)  # Connect signal to slot
        threading.Thread(target=self.update_img).start()

    @pyqtSlot(QPixmap)
    def update_label(self, pixmap):
        self.__label.setPixmap(pixmap.scaled(self.__label.size(), Qt.KeepAspectRatio))

    def update_img(self):
        while self.__run:
            img_data = self.__server_client_connection.get_image()
            if img_data:
                image = Image.open(io.BytesIO(img_data))
                qt_image = QImage(image.tobytes(), image.width, image.height, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_image)
                self.update_image_signal.emit(pixmap)  # Emit signal with the updated pixmap

    def stop(self):
        self.__run = False
        if self.__name in self.__users_with_share_screen_open:
            self.__users_with_share_screen_open.remove(self.__name)
        self.close()
