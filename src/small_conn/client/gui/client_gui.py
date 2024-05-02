import sys
import threading
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget

from src.client.client_user_database import ClientUserDatabase, ValueTypes


class ClientUserGui(QMainWindow):
    def __init__(self, data_base: ClientUserDatabase):
        super().__init__()

        self.__run = True
        self.__data_base = data_base
        self.__data_base.set_value(ValueTypes.IS_GUI_CONNECTED, True)

        self.setWindowTitle(f"Control Board")
        self.setFixedSize(300, 150)  # Set the fixed size of the window

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

        self.data_base_update_thread = threading.Thread(target=self.database_update)
        self.data_base_update_thread.start()

    def toggle_keyboard_button(self):
        keyboard_status = self.__data_base.get_value(ValueTypes.KEYBOARD_INPUT)
        keyboard_status = not keyboard_status
        self.__data_base.set_value(ValueTypes.KEYBOARD_INPUT, keyboard_status)
        print(self.__data_base.__str__())

    def toggle_screen_share_button(self):
        screen_share_status = self.__data_base.get_value(ValueTypes.SCREEN_SHARE_INPUT)
        screen_share_status = not screen_share_status
        self.__data_base.set_value(ValueTypes.SCREEN_SHARE_INPUT, screen_share_status)
        print(self.__data_base.__str__())

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
        self.__data_base.set_value(ValueTypes.IS_GUI_CONNECTED, False)
        event.accept()

    def database_update(self):
        # # default
        self.previous_database_is_keyboard_input = False
        self.previous_database_is_screen_share_input = False

        # wait to the conn to start
        while not self.__data_base.get_value(ValueTypes.IS_CONN_CONNECTED):
            pass

        while self.__run:
            database_is_keyboard_input = self.__data_base.get_value(ValueTypes.KEYBOARD_INPUT)
            database_is_screen_share_input = self.__data_base.get_value(ValueTypes.SCREEN_SHARE_INPUT)
            if not self.__data_base.get_value(ValueTypes.IS_CONN_CONNECTED):
                self.disconnect_user()

            if database_is_keyboard_input != self.previous_database_is_keyboard_input:
                self.set_indicator(database_is_keyboard_input, self.keyboard_indicator)

            if database_is_screen_share_input != self.previous_database_is_screen_share_input:
                self.set_indicator(database_is_screen_share_input, self.screen_share_indicator)

            self.previous_database_is_keyboard_input = database_is_keyboard_input
            self.previous_database_is_screen_share_input = database_is_screen_share_input


class ClientUserGuiApplication(QApplication):
    def __init__(self, database: ClientUserDatabase):
        self.__database = database
        super().__init__(sys.argv)
        self.window = ClientUserGui(database)
        self.window.show()
        sys.exit(self.exec_())

