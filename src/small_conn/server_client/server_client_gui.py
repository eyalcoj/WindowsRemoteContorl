import sys
import threading
import random
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget

from src.small_conn.client.client_data_saver import KeyValue


class ServerUserGui(QWidget):
    def __init__(self, name, user_data_saver, users_data_saver):
        super().__init__()
        self.__name = name
        self.__user_data_saver = user_data_saver
        self.__users_data_saver = users_data_saver

        self.__run = True

        self.setWindowTitle(f"{self.__name}")
        self.setFixedSize(300, 150)  # Set the fixed size of the window

        # Layout setup
        main_layout = QVBoxLayout(self)  # Set the main layout directly to the widget

        # Screen Share setup
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

        # Keyboard setup
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

        # Label for keyboard input
        self.keyboard_output_label = QLabel("Input:")
        self.keyboard_output_label.setWordWrap(True)
        main_layout.addWidget(self.keyboard_output_label)

        # Disconnect button
        self.disconnect_button = QPushButton('Disconnect')
        main_layout.addWidget(self.disconnect_button)

        print("start connect buttons")
        # Connecting buttons to methods
        self.keyboard_button.clicked.connect(lambda: self.want_toggle_keyboard_button())
        self.screen_share_button.clicked.connect(lambda: self.want_toggle_screen_share_button())
        self.disconnect_button.clicked.connect(self.disconnect)

        threading.Thread(target=self.data_saver_update).start()

    # Define other methods like database_update, want_toggle_keyboard_button, want_toggle_screen_share_button here...

    def want_toggle_keyboard_button(self):
        print("1")

    def want_toggle_screen_share_button(self):
        print("2")

    def set_indicator(self, is_green, indicator):
        if is_green:
            indicator.setStyleSheet("background-color: green; border-radius: 10px;")
        else:
            indicator.setStyleSheet("background-color: red; border-radius: 10px;")

    def disconnect(self):
        print("Disconnected!2")
        self.__run = False
        self.__users_data_saver.remove(self.__name)
        self.close()

    #     it goes to the closeEvent before closing

    def closeEvent(self, event):
        print("X closing2")
        event.accept()

    def get_is_run(self):
        return self.__run

    def data_saver_update(self):
        prev_keyboard = False
        prev_share_Screen = False
        while self.__run:
            current_keyboard = self.__user_data_saver.get_value(KeyValue.IS_CLIENT_KEYBOARD)
            current_share_Screen = self.__user_data_saver.get_value(KeyValue.IS_CLIENT_SHARE_SCREEN)

            if prev_keyboard != current_keyboard:
                self.set_indicator(current_keyboard, self.keyboard_indicator)
                prev_keyboard = current_keyboard

            if prev_share_Screen != current_share_Screen:
                self.set_indicator(current_share_Screen, self.screen_share_indicator)
                prev_share_Screen = current_share_Screen


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ServerUserGui()
    window.show()

    sys.exit(app.exec_())
