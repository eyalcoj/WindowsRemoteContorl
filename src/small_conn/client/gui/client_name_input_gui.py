import sys
import time

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

from src.small_conn.client.client_connection import ClientServerConnection
from src.small_conn.client.client_connection_warper import ClientConnectionWarper


class NameInputGUI(QWidget):
    def __init__(self, client_connection_warper: ClientConnectionWarper):
        super().__init__()
        self.client_connection_warper = client_connection_warper
        self.name = ""
        self.initUI()

    def initUI(self):
        # Create a QVBoxLayout instance
        self.setWindowTitle('name input')
        layout = QVBoxLayout()

        # Create a QLineEdit widget for name input
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter your name here")


        # Create another QLabel for displaying the output
        self.result_label = QLabel("pleas enter your name")

        # Create a QPushButton and set its text
        self.button = QPushButton("Click me!", self)
        self.button.clicked.connect(self.on_click)

        # Add widgets to the layout
        layout.addWidget(self.name_input)
        layout.addWidget(self.button)
        layout.addWidget(self.result_label)

        # Set the layout on the application's window
        self.setLayout(layout)

    def on_click(self):
        # Get the text from the QLineEdit widget
        name = self.name_input.text()
        if name.replace(" ", "") != "":
            print("000")
            self.client_connection_warper.input_user_name(name)
            print("111")
            feedback = self.client_connection_warper.feedback
            print("222")
            self.result_label.setText(f"{feedback}")
            print("333")
            QApplication.processEvents()
            print("444")
            if feedback == "The name is all ready in use":
                pass
            elif feedback == "The name is not in use":
                self.name = name
                self.close_gui()
            print("555")
        # Set the text of result_label to input_text

    def close_gui(self):
        print("Close GUI!")
        self.close()

    #     it goes to the closeEvent before closing

    def closeEvent(self, event):
        print("X closing")
        event.accept()

    def get_name(self):
        return self.name

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = NameInputGUI()
    ex.show()
    sys.exit(app.exec_())
