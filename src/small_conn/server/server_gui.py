import sys
import threading
import time

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QLabel, QMainWindow, QPushButton

from src.database.securedDataBase import SecuredDataBase
from src.server.database.server_database_connection import ServerDatabaseConnection, ValueTypes
from src.utils.utils import find_changes_between_lists


#
# class UserDetailsWindow(QMainWindow):
#     def __init__(self, user_name):
#         super().__init__()
#         self.setWindowTitle(user_name)
#         self.setGeometry(100, 100, 200, 100)  # Set position and dimensions (x, y, width, height)
#         self.show()

class ServerGui(QMainWindow):
    def __init__(self, connection_database: ServerDatabaseConnection, users_database: SecuredDataBase):
        super().__init__()
        self.__run = True
        self.__connection_database = connection_database
        self.__users_database = users_database
        self.__connection_database.set_value(ValueTypes.IS_GUI_CONNECTED, True)
        self.initUI()
        self.data_base_update_thread = threading.Thread(target=self.database_update)
        self.data_base_update_thread.start()

    def initUI(self):
        # Create central widget and layout
        central_widget = QWidget()   # Central widget
        layout = QVBoxLayout()       # Layout for central widget

        # Label
        self.label = QLabel("Users Connected:")
        layout.addWidget(self.label)

        # List widget
        self.listWidget = QListWidget()
        self.listWidget.itemClicked.connect(self.onItemClicked)  # Connect the itemClicked signal to the slot
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
        self.__connection_database.set_value(ValueTypes.IS_GUI_CONNECTED, False)
        self.__run = False
        self.listWidget.clear()
        keys = self.__users_database.get_keys()
        for _ in keys:
            user = self.__users_database.get_value(_)
            if user:
                print("user is not null")
                user_app = user.get_server_user_gui_application()
                if user_app.get_window():
                    user_app.disconnect_window()

        event.accept()
        print("X closing")

    def onItemClicked(self, item):
        user_name = item.text()
        user_gui_app = self.__users_database.get_value(user_name).get_server_user_gui_application()
        print(user_gui_app)
        if not user_gui_app.get_window() or not user_gui_app.get_window().get_is_run():
            print("click")
            thread_app = threading.Thread(target=self.__users_database.get_value(user_name).get_server_user_gui_application().show_window())
            thread_app.start()

    def database_update(self):
        # # default
        self.previous_users_names = []

        # wait to the conn to start
        while not self.__connection_database.get_value(ValueTypes.IS_CONN_CONNECTED):
            print("in the loop")
            pass

        while self.__run:
            users_names = self.__users_database.get_keys()
            # print(users_names)
            if not self.__connection_database.get_value(ValueTypes.IS_CONN_CONNECTED):
                self.disconnect()

            added, removed = find_changes_between_lists(self.previous_users_names, users_names)
            if len(removed) > 0:
                for _ in removed:
                    self.removeUser(_)

            if len(added) > 0:
                for _ in added:
                    self.addUser(_)

            self.previous_users_names = users_names


class ServerGuiApplication(QApplication):
    def __init__(self, connection_database: ServerDatabaseConnection, users_database: SecuredDataBase):
        super().__init__(sys.argv)
        self.__connection_database = connection_database
        self.__users_database = users_database
        self.window = ServerGui(connection_database, users_database)
        self.window.show()
        self.quit()
        sys.exit(self.exec_())


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = ServerGui(ServerDatabaseConnection())
#     ex.show()
#     sys.exit(app.exec_())
