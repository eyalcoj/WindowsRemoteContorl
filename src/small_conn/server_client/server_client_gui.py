import sys
import threading

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QMainWindow

from src.share_screen_conn.server_client.screen_share_gui import ScreenShareGui
from src.share_screen_conn.server_client.screen_share_server_client_connection import ScreenShareServerClientConnection
from src.small_conn.server_client.server_client_data_saver import KeyValue


class ServerUserGui(QMainWindow):
    open_screen_share_signal = pyqtSignal()
    close_screen_share_signal = pyqtSignal()

    def __init__(self, name, user_data_saver, users_data_saver,
                 user_with_share_screen_conn: ScreenShareServerClientConnection, users_with_share_screen_open,
                 user_with_open_gui):
        super().__init__()
        self.__name = name
        self.__user_data_saver = user_data_saver
        self.__user_with_share_screen_conn = user_with_share_screen_conn
        self.__users_data_saver = users_data_saver
        self.__users_with_share_screen_open = users_with_share_screen_open
        self.__user_with_open_gui = user_with_open_gui
        self.win = None
        self.__run = True

        self.setWindowTitle(f"{self.__name}")
        self.setFixedSize(300, 150)
        self.setWindowIcon(QIcon(r'src/imgs/user-removebg-preview.png'))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        self.screen_share_button = QPushButton('Screen Share')
        self.screen_share_button.setStyleSheet("text-align: left;")
        self.screen_share_indicator = QLabel()
        self.screen_share_indicator.setFixedSize(20, 20)
        self.screen_share_indicator.setStyleSheet("background-color: red; border-radius: 10px;")
        self.want_screen_share_indicator = QLabel()
        self.want_screen_share_indicator.setFixedSize(20, 20)
        self.want_screen_share_indicator.setStyleSheet("background-color: red; border-radius: 10px;")
        screen_share_row = QHBoxLayout()
        screen_share_row.addWidget(self.screen_share_button, 2)
        screen_share_row.addWidget(self.want_screen_share_indicator, 1)
        screen_share_row.addWidget(self.screen_share_indicator)
        screen_share_row.setStretch(0, 1)
        main_layout.addLayout(screen_share_row)

        self.keyboard_button = QPushButton('Keyboard')
        self.keyboard_button.setStyleSheet("text-align: left;")
        self.want_keyboard_indicator = QLabel()
        self.want_keyboard_indicator.setFixedSize(20, 20)
        self.want_keyboard_indicator.setStyleSheet("background-color: red; border-radius: 10px;")
        self.keyboard_indicator = QLabel()
        self.keyboard_indicator.setFixedSize(20, 20)
        self.keyboard_indicator.setStyleSheet("background-color: red; border-radius: 10px;")
        keyboard_row = QHBoxLayout()
        keyboard_row.addWidget(self.keyboard_button, 2)
        keyboard_row.addWidget(self.want_keyboard_indicator, 1)
        keyboard_row.addWidget(self.keyboard_indicator)
        keyboard_row.setStretch(0, 1)
        main_layout.addLayout(keyboard_row)

        self.disconnect_button = QPushButton('Disconnect')
        main_layout.addWidget(self.disconnect_button)

        self.keyboard_button.clicked.connect(lambda: self.want_toggle_keyboard_button())
        self.screen_share_button.clicked.connect(lambda: self.want_toggle_screen_share_button())
        self.disconnect_button.clicked.connect(self.disconnect)

        self.open_screen_share_signal.connect(self.open_screen_share_gui)
        self.close_screen_share_signal.connect(self.close_screen_share_gui)
        threading.Thread(target=self.data_saver_update).start()

    def want_toggle_keyboard_button(self):
        current_status = self.__user_data_saver.get_value(KeyValue.IS_SERVER_KEYBOARD)
        self.__user_data_saver.set_value(KeyValue.IS_SERVER_KEYBOARD, not current_status)

    def want_toggle_screen_share_button(self):
        current_status = self.__user_data_saver.get_value(KeyValue.IS_SERVER_SHARE_SCREEN)
        self.__user_data_saver.set_value(KeyValue.IS_SERVER_SHARE_SCREEN, not current_status)

    @staticmethod
    def set_indicator(is_green, indicator):
        if is_green:
            indicator.setStyleSheet("background-color: green; border-radius: 10px;")
        else:
            indicator.setStyleSheet("background-color: red; border-radius: 10px;")

    def disconnect(self):
        # it goes to the closeEvent before closing
        print("Disconnected!24")
        self.__users_data_saver.remove(self.__name)
        self.close()

    def closeEvent(self, event):
        self.__run = False
        self.__user_data_saver.set_value(KeyValue.IS_SERVER_KEYBOARD, False)
        self.__user_data_saver.set_value(KeyValue.IS_SERVER_SHARE_SCREEN, False)
        self.__user_with_open_gui.remove(self.__name)
        if self.win:
            self.win.stop()
        self.__user_with_share_screen_conn.send_disconnect_request()
        event.accept()

    def get_is_run(self):
        return self.__run

    def set_is_run(self, is_run):
        self.__run = is_run

    def open_screen_share_gui(self):
        self.win = ScreenShareGui(self.__user_with_share_screen_conn, self.__name, self.__users_with_share_screen_open,
                                  self.__user_data_saver)
        self.__user_with_share_screen_conn.send_connect_request()
        self.win.show()

    def close_screen_share_gui(self):
        self.win.stop()
        self.__user_with_share_screen_conn.send_disconnect_request()

    def data_saver_update(self):
        prev_keyboard = False
        prev_share_screen = False
        prev_my_keyboard = False
        prev_my_share_screen = False
        while self.__run:
            current_keyboard = self.__user_data_saver.get_value(KeyValue.IS_CLIENT_KEYBOARD)
            current_share_screen = self.__user_data_saver.get_value(KeyValue.IS_CLIENT_SHARE_SCREEN)
            current_my_keyboard = self.__user_data_saver.get_value(KeyValue.IS_SERVER_KEYBOARD)
            current_my_share_screen = self.__user_data_saver.get_value(KeyValue.IS_SERVER_SHARE_SCREEN)

            if prev_keyboard != current_keyboard:
                self.set_indicator(current_keyboard, self.keyboard_indicator)
                prev_keyboard = current_keyboard

            if prev_share_screen != current_share_screen:
                self.set_indicator(current_share_screen, self.screen_share_indicator)
                prev_share_screen = current_share_screen

            if prev_my_keyboard != current_my_keyboard:
                self.set_indicator(current_my_keyboard, self.want_keyboard_indicator)
                prev_my_keyboard = current_my_keyboard

            if prev_my_share_screen != current_my_share_screen:
                self.set_indicator(current_my_share_screen, self.want_screen_share_indicator)
                prev_my_share_screen = current_my_share_screen
            if current_share_screen and current_my_share_screen:
                if self.__users_with_share_screen_open.get_value(self.__name) is None:
                    self.__users_with_share_screen_open.set_value(self.__name, "_")
                    self.open_screen_share_signal.emit()
            else:
                user = self.__users_with_share_screen_open.get_value(self.__name)
                if user is not None and user != "":
                    self.__users_with_share_screen_open.remove(self.__name)
                    if self.win:
                        self.close_screen_share_signal.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ServerUserGui()
    window.show()

    sys.exit(app.exec_())
