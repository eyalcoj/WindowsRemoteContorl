import sys
import threading
import time

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget

from src.small_conn.client.client_data_saver import ClientDataSaver, KeyValue


class ClientUserGui(QMainWindow):
    def __init__(self, name, client_data_saver: ClientDataSaver):
        super().__init__()
        self.__name = name
        self.__client_data_saver = client_data_saver
        self.__run = True

        self.setWindowTitle(f"{self.__name}")
        self.setFixedSize(300, 150)  # Set the fixed size of the window
        self.setWindowIcon(QIcon(r'src/imgs/user-removebg-preview.png'))

        # Layout and widget setup
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()

        self.screen_share_button = QPushButton('screen share button', self)
        self.screen_share_button.setStyleSheet("text-align: left;")  # Align text to the left
        self.screen_share_indicator = QLabel()
        self.screen_share_indicator.setFixedSize(20, 20)
        self.screen_share_indicator.setStyleSheet("background-color: red; border-radius: 10px;")
        self.screen_share_row = QHBoxLayout()
        self.screen_share_row.addWidget(self.screen_share_button, 1)
        self.screen_share_row.addWidget(self.screen_share_indicator)
        self.screen_share_row.setStretch(0, 1)  # Give more space to the button in the layout
        self.main_layout.addLayout(self.screen_share_row)

        self.keyboard_button = QPushButton('keyboard button', self)
        self.keyboard_button.setStyleSheet("text-align: left;")  # Align text to the left
        self.keyboard_indicator = QLabel()
        self.keyboard_indicator.setFixedSize(20, 20)
        self.keyboard_indicator.setStyleSheet("background-color: red; border-radius: 10px;")
        self.keyboard_row = QHBoxLayout()
        self.keyboard_row.addWidget(self.keyboard_button, 1)
        self.keyboard_row.addWidget(self.keyboard_indicator)
        self.keyboard_row.setStretch(0, 1)  # Give more space to the button in the layout
        self.main_layout.addLayout(self.keyboard_row)

        # Disconnect button setup
        self.disconnect_button = QPushButton('Disconnect')
        self.main_layout.addWidget(self.disconnect_button)

        # Set central widget
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # Connecting buttons to methods
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

    def set_indicator(self, is_green, indicator):
        if is_green:
            indicator.setStyleSheet("background-color: green; border-radius: 10px;")
        else:
            indicator.setStyleSheet("background-color: red; border-radius: 10px;")

    def append_char_to_label(self, char: str):
        self.__label_text += char
        if len(self.__label_text) > 39:
            self.__label_text = self.__label_text[1:]
        self.keyboard_output_label.setText(self.__label_text)

    def disconnect_user(self):
        print("Disconnected!")
        self.close()

    #     it goes to the closeEvent before closing

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






if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ClientUserGui()
    win.show()
    sys.exit(app.exec_())
