import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton


class NameInputGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create a QVBoxLayout instance
        layout = QVBoxLayout()

        # Create a QLineEdit widget for name input
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter your name here")

        # Create a QPushButton and set its text
        self.button = QPushButton("Click me!", self)
        self.button.clicked.connect(self.on_click)

        # Create another QLabel for displaying the output
        self.result_label = QLabel("")

        # Add widgets to the layout
        layout.addWidget(self.name_input)
        layout.addWidget(self.button)
        layout.addWidget(self.result_label)

        # Set the layout on the application's window
        self.setLayout(layout)
        self.setWindowTitle('name input')

    def on_click(self):
        # Get the text from the QLineEdit widget
        input_text = self.name_input.text()

        # Set the text of result_label to input_text
        self.result_label.setText(f"You entered: {input_text}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = NameInputGUI()
    ex.show()
    sys.exit(app.exec_())
