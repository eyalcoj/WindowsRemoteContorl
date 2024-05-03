import sys
import threading

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QLabel, QMainWindow, QPushButton

from src.data_saver.secured_data_saver import SecuredDataSaver
from src.small_conn.server_client.server_client_gui import ServerUserGui
from src.utils.utils import find_changes_between_lists


class ServerGui(QMainWindow):
    def __init__(self, users_data_saver: SecuredDataSaver):
        super().__init__()
        self.__run = True
        self.__users_data_saver = users_data_saver
        self.initUI()
        self.__user_with_open_gui = SecuredDataSaver()

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
        self.listWidget.itemDoubleClicked.connect(self.onItemClicked)  # Connect the itemClicked signal to the slot
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

    #     it goes to the closeEvent before closing

    def closeEvent(self, event):
        self.__run = False
        self.listWidget.clear()

        event.accept()
        print("X closing")

    def onItemClicked(self, item):
        user_name = item.text()
        # print(f"{self.__user_with_open_gui.get_value(user_name)}")
        if self.__user_with_open_gui.get_value(user_name) is None:
            # print("pjo")
            self.__user_with_open_gui.set_value(user_name, "_")
            win = ServerUserGui(user_name, self.__users_data_saver.get_value(user_name), self.__users_data_saver)
            win.show()
            threading.Thread(target=self.check_gui, args=(win, user_name)).start()

    def check_gui(self, win, user_name):
        while win.get_is_run():
            if not self.__run:
                break
        self.__user_with_open_gui.remove(user_name)

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
