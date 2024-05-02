import sys
import threading
import random
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget

from src.server.database.server_user_database import ServerUserDatabase, ValueTypes


class ServerUserGui(QWidget):
    def __init__(self, data_base: ServerUserDatabase):
        super().__init__()

        self.__run = True
        self.__data_base = data_base
        self.__data_base.set_value(ValueTypes.IS_GUI_CONNECTED, True)
        self.__data_base.set_value(ValueTypes.IS_GUI_CONNECTED_AND_STAY, True)

        self.setWindowTitle("Control Board")
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

        # Thread to update database values
        self.data_base_update_thread = threading.Thread(target=self.database_update)
        self.data_base_update_thread.start()

    # Define other methods like database_update, want_toggle_keyboard_button, want_toggle_screen_share_button here...

    def want_toggle_keyboard_button(self):
        print("1")
        want_keyboard_status = self.__data_base.get_value(ValueTypes.WANT_KEYBOARD_INPUT)
        want_keyboard_status = not want_keyboard_status
        self.__data_base.set_value(ValueTypes.WANT_KEYBOARD_INPUT, want_keyboard_status)
        print(self.__data_base.__str__())

    def want_toggle_screen_share_button(self):
        print("2")
        want_screen_share_status = self.__data_base.get_value(ValueTypes.WANT_SCREEN_SHARE_INPUT)
        want_screen_share_status = not want_screen_share_status
        self.__data_base.set_value(ValueTypes.WANT_SCREEN_SHARE_INPUT, want_screen_share_status)
        print(self.__data_base.__str__())

    def set_indicator(self, is_green, indicator):
        if is_green:
            indicator.setStyleSheet("background-color: green; border-radius: 10px;")
        else:
            indicator.setStyleSheet("background-color: red; border-radius: 10px;")

    def disconnect(self):
        print("Disconnected!2")
        self.__data_base.set_value(ValueTypes.IS_GUI_CONNECTED_AND_STAY, False)
        self.close()

    #     it goes to the closeEvent before closing

    def closeEvent(self, event):
        print("X closing2")
        self.__run = False
        event.accept()

    def get_is_run(self):
        return self.__run

    def database_update(self):

        # default
        self.previous_database_is_keyboard_input = False
        self.previous_database_is_screen_share_input = False
        self.want_previous_database_is_keyboard_input = False
        self.want_previous_database_is_screen_share_input = False

        # wait to the conn to start
        while not self.__data_base.get_value(ValueTypes.IS_CONN_CONNECTED):
            pass

        while self.__run:
            database_is_keyboard_input = self.__data_base.get_value(ValueTypes.KEYBOARD_INPUT)
            database_is_screen_share_input = self.__data_base.get_value(ValueTypes.SCREEN_SHARE_INPUT)
            want_database_is_keyboard_input = self.__data_base.get_value(ValueTypes.WANT_KEYBOARD_INPUT)
            want_database_is_screen_share_input = self.__data_base.get_value(ValueTypes.WANT_SCREEN_SHARE_INPUT)
            if not self.__data_base.get_value(ValueTypes.IS_CONN_CONNECTED):
                self.disconnect()

            if database_is_keyboard_input != self.previous_database_is_keyboard_input:
                self.set_indicator(database_is_keyboard_input, self.keyboard_indicator)
                if not database_is_keyboard_input:
                    self.__label_text = ""
                    self.keyboard_output_label.setText("Input: ")

            if database_is_screen_share_input != self.previous_database_is_screen_share_input:
                self.set_indicator(database_is_screen_share_input, self.screen_share_indicator)

            if want_database_is_keyboard_input != self.want_previous_database_is_keyboard_input:
                print("in1")
                self.set_indicator(want_database_is_keyboard_input, self.want_keyboard_indicator)
                if not want_database_is_keyboard_input:
                    self.__label_text = ""
                    self.keyboard_output_label.setText("Input: ")

            if want_database_is_screen_share_input != self.want_previous_database_is_screen_share_input:
                print("in2")
                self.set_indicator(want_database_is_screen_share_input, self.want_screen_share_indicator)

            self.previous_database_is_keyboard_input = database_is_keyboard_input
            self.previous_database_is_screen_share_input = database_is_screen_share_input
            self.want_previous_database_is_keyboard_input = want_database_is_keyboard_input
            self.want_previous_database_is_screen_share_input = want_database_is_screen_share_input


class ServerUserGuiApplication:
    def __init__(self, database: ServerUserDatabase):
        self.__database = database
        self.window = None

    def show_window(self):
        print("in show window")
        # put in thread
        self.window = ServerUserGui(self.__database)
        self.window.show()

    def disconnect_window(self):
        print("disconnect window")
        self.window.close()

    def get_window(self):
        return self.window


if __name__ == "__main__":
    user_database = ServerUserDatabase()
    user_database.set_value(ValueTypes.IS_CONN_CONNECTED, True)

    app = QApplication(sys.argv)

    window = ServerUserGui(user_database)
    window.show()

    sys.exit(app.exec_())
