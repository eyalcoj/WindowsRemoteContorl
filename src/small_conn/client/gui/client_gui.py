import threading

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget

from src.small_conn.client.client_data_saver import ClientDataSaver, KeyValue


class Constance:
    SCREEN_WIDTH = 300
    SCREEN_HEIGHT = 150
    INDICATOR_WIDTH = 20
    INDICATOR_HEIGHT = 20


class ClientUserGui(QMainWindow):
    def __init__(self, name, client_data_saver: ClientDataSaver):
        super().__init__()
        self.__name = name
        self.__client_data_saver = client_data_saver
        self.__run = True

        self.setWindowTitle(f"{self.__name}")
        self.setFixedSize(Constance.SCREEN_WIDTH, Constance.SCREEN_HEIGHT)
        self.setWindowIcon(QIcon(r'src/imgs/user-removebg-preview.png'))

        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()

        self.screen_share_button = QPushButton('screen share button', self)
        self.screen_share_button.setStyleSheet("text-align: left;")
        self.screen_share_indicator = QLabel()
        self.screen_share_indicator.setFixedSize(Constance.INDICATOR_WIDTH, Constance.INDICATOR_HEIGHT)
        self.screen_share_indicator.setStyleSheet("background-color: red; border-radius: 10px;")
        self.screen_share_row = QHBoxLayout()
        self.screen_share_row.addWidget(self.screen_share_button, 1)
        self.screen_share_row.addWidget(self.screen_share_indicator)
        self.screen_share_row.setStretch(0, 1)
        self.main_layout.addLayout(self.screen_share_row)

        self.keyboard_button = QPushButton('keyboard button', self)
        self.keyboard_button.setStyleSheet("text-align: left;")
        self.keyboard_indicator = QLabel()
        self.keyboard_indicator.setFixedSize(Constance.INDICATOR_WIDTH, Constance.INDICATOR_HEIGHT)
        self.keyboard_indicator.setStyleSheet("background-color: red; border-radius: 10px;")
        self.keyboard_row = QHBoxLayout()
        self.keyboard_row.addWidget(self.keyboard_button, 1)
        self.keyboard_row.addWidget(self.keyboard_indicator)
        self.keyboard_row.setStretch(0, 1)
        self.main_layout.addLayout(self.keyboard_row)

        self.disconnect_button = QPushButton('Disconnect')
        self.main_layout.addWidget(self.disconnect_button)

        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        self.keyboard_button.clicked.connect(lambda: self.toggle_keyboard_button())
        self.screen_share_button.clicked.connect(lambda: self.toggle_screen_share_button())
        self.disconnect_button.clicked.connect(self.disconnect_user)

        threading.Thread(target=self.data_saver_update).start()

    def toggle_keyboard_button(self):
        current_status = self.__client_data_saver.get_value(KeyValue.IS_CLIENT_KEYBOARD)
        self.__client_data_saver.set_value(KeyValue.IS_CLIENT_KEYBOARD, not current_status)

    def toggle_screen_share_button(self):
        current_status = self.__client_data_saver.get_value(KeyValue.IS_CLIENT_SHARE_SCREEN)
        self.__client_data_saver.set_value(KeyValue.IS_CLIENT_SHARE_SCREEN, not current_status)

    @staticmethod
    def set_indicator(is_green, indicator):
        if is_green:
            indicator.setStyleSheet("background-color: green; border-radius: 10px;")
        else:
            indicator.setStyleSheet("background-color: red; border-radius: 10px;")

    def disconnect_user(self):
        # it goes to the closeEvent before closing
        print("Disconnected!")
        self.close()

    def closeEvent(self, event):
        print("X closing")
        self.__run = False
        event.accept()

    def data_saver_update(self):
        prev_keyboard = False
        prev_share_Screen = False
        while self.__run:
            current_keyboard = self.__client_data_saver.get_value(KeyValue.IS_CLIENT_KEYBOARD)
            current_share_Screen = self.__client_data_saver.get_value(KeyValue.IS_CLIENT_SHARE_SCREEN)

            if prev_keyboard != current_keyboard:
                self.set_indicator(current_keyboard, self.keyboard_indicator)
                prev_keyboard = current_keyboard

            if prev_share_Screen != current_share_Screen:
                self.set_indicator(current_share_Screen, self.screen_share_indicator)
                prev_share_Screen = current_share_Screen
