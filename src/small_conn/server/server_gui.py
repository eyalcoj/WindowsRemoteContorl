import sys
import threading

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QLabel, QMainWindow, QPushButton

from src.data_saver.secured_data_saver import SecuredDataSaver
from src.small_conn.server_client.server_client_gui import ServerUserGui
from src.utils.utils import find_changes_between_lists


class ServerGui(QMainWindow):
    def __init__(self, users_data_saver: SecuredDataSaver, user_with_share_screen: SecuredDataSaver):
        super().__init__()
        self.__run = True
        self.__users_data_saver = users_data_saver
        self.__users_with_share_screen = user_with_share_screen
        self.initUI()
        self.__user_with_open_gui = SecuredDataSaver()
        self.__users_with_share_screen_open = SecuredDataSaver()

        threading.Thread(target=self.data_saver_update).start()

    def initUI(self):
        # Create central widget and layout
        central_widget = QWidget()  # Central widget
        layout = QVBoxLayout()  # Layout for central widget

        # Label
        self.label = QLabel("Users Connected:")
        layout.addWidget(self.label)

        # List widget
        self.listWidget = QListWidget()
        self.listWidget.itemDoubleClicked.connect(self.on_item_clicked)  # Connect the itemClicked signal to the slot
        layout.addWidget(self.listWidget)

        # Disconnect button setup
        self.disconnect_button = QPushButton('Disconnect')
        self.disconnect_button.clicked.connect(self.disconnect)
        layout.addWidget(self.disconnect_button)

        # Set central widget and layout
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setWindowTitle("Remote Control System Users")

    def addUser(self, name: str):
        if name:  # Only add if the text is not empty
            self.listWidget.addItem(name)

    def removeUser(self, name: str):
        if name:  # Only add if the text is not empty
            items = self.listWidget.findItems(name, Qt.MatchExactly)
            if items:
                for item in items:
                    row = self.listWidget.row(item)
                    self.listWidget.takeItem(row)

    def disconnect(self):
        print("Disconnected!")
        self.close()


    def closeEvent(self, event):
        self.__run = False
        self.listWidget.clear()
        keys = self.__user_with_open_gui.get_keys()
        for _ in keys:
            self.__user_with_open_gui.get_value(_).close()
        event.accept()
        print("X closing")

    def on_item_clicked(self, item):
        user_name = item.text()
        print(self.__user_with_open_gui.get_value(user_name))
        if self.__user_with_open_gui.get_value(user_name) is None:
            print(self.__users_with_share_screen.__str__())
            win = ServerUserGui(user_name, self.__users_data_saver.get_value(user_name), self.__users_data_saver,
                                self.__users_with_share_screen.get_value(user_name), self.__users_with_share_screen_open
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
                    self.removeUser(_)

            if len(added) > 0:
                for _ in added:
                    self.addUser(_)

            previous_users_names = users_names


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ServerGui()
    ex.show()
    sys.exit(app.exec_())
