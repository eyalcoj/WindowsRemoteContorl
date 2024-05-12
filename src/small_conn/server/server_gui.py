import threading

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLabel, QMainWindow, QPushButton

from src.data_saver.secured_data_saver import SecuredDataSaver
from src.small_conn.server_client.server_client_gui import ServerUserGui
from src.utils.utils import find_changes_between_lists


class Constance:
    SCREEN_WIDTH = 300
    SCREEN_HEIGHT = 250


class ServerGui(QMainWindow):
    def __init__(self, users_data_saver: SecuredDataSaver, users_share_screen_conn: SecuredDataSaver):
        super().__init__()
        self.label = None
        self.list_widget = None
        self.disconnect_button = None
        self.__run = True
        self.__users_data_saver = users_data_saver
        self.__users_share_screen_conn = users_share_screen_conn
        self.initUI()
        self.__user_with_open_gui = SecuredDataSaver()
        self.__users_with_share_screen_open = SecuredDataSaver()

        threading.Thread(target=self.data_saver_update).start()

    def initUI(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        self.setFixedSize(Constance.SCREEN_WIDTH, Constance.SCREEN_WIDTH)
        self.setWindowIcon(QIcon(r'src/imgs/users-removebg-preview.png'))
        self.setWindowTitle("Users")

        self.label = QLabel("Users Connected:")
        layout.addWidget(self.label)

        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.on_item_clicked)
        layout.addWidget(self.list_widget)

        self.disconnect_button = QPushButton('Disconnect')
        self.disconnect_button.clicked.connect(self.disconnect)
        layout.addWidget(self.disconnect_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def add_user(self, name: str):
        if name:
            self.list_widget.addItem(name)

    def remove_user(self, name: str):
        if name:
            gui = self.__user_with_open_gui.get_value(name)
            if gui:
                gui.close()
            items = self.list_widget.findItems(name, Qt.MatchExactly)
            if items:
                for item in items:
                    row = self.list_widget.row(item)
                    self.list_widget.takeItem(row)

    def disconnect(self):
        # it goes to the closeEvent before closing
        print("Disconnected!")
        self.close()

    def closeEvent(self, event):
        self.__run = False
        self.list_widget.clear()
        keys = self.__user_with_open_gui.get_keys()
        for _ in keys:
            self.__user_with_open_gui.get_value(_).close()
        event.accept()
        print("X closing")

    def on_item_clicked(self, item):
        user_name = item.text()
        if self.__user_with_open_gui.get_value(user_name) is None:
            win = ServerUserGui(user_name, self.__users_data_saver.get_value(user_name), self.__users_data_saver,
                                self.__users_share_screen_conn.get_value(user_name), self.__users_with_share_screen_open
                                , self.__user_with_open_gui)
            self.__user_with_open_gui.set_value(user_name, win)
            win.show()

    def data_saver_update(self):
        previous_users_names = []
        while self.__run:
            users_names = self.__users_data_saver.get_keys()
            added, removed = find_changes_between_lists(previous_users_names, users_names)
            if len(removed) > 0:
                for _ in removed:
                    self.remove_user(_)

            if len(added) > 0:
                for _ in added:
                    self.add_user(_)

            previous_users_names = users_names
