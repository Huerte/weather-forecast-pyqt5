from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox, QSizePolicy
from PyQt5.QtCore import Qt


class LoginWindow:
    def __init__(self, stack_widget):
        self.stack_widget = stack_widget
        self.name_input = ""
        self.password_input = ""

    def display(self):
        window2 = QWidget()

        window = QWidget()
        layout = QVBoxLayout()

        header = QLabel("Login Account")
        layout.addWidget(header, alignment=Qt.AlignBottom | Qt.AlignHCenter)  # Adjust as needed

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your username")
        layout.addWidget(self.name_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        layout.addWidget(self.password_input)

        login_button = QPushButton("Login")
        login_button.clicked.connect(lambda: self.proceed_to_home_page(window))
        layout.addWidget(login_button)

        window.setLayout(layout)

        layout2 = QVBoxLayout()
        layout2.addWidget(window2, alignment=Qt.AlignBottom | Qt.AlignHCenter)

        return window

    def proceed_to_home_page(self, window):
        if self.name_input.text().strip() == "" or self.password_input.text().strip() == "":
            self.show_error_message(window, "Hayap kaw Loy?", "Empty input field detected!")

        elif self.name_input.text() == "ako" and self.password_input.text() == "password":
            self.stack_widget.setCurrentIndex(2)
        else:
            self.show_error_message(window, "Error Loy", "User Does Not Exist!")
            self.clear_input_fields()

    def clear_input_fields(self):
        self.name_input.clear()
        self.password_input.clear()

    @staticmethod
    def show_error_message(window, title, message):
        error_box = QMessageBox(window)
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle(title)
        error_box.setText(message)
        error_box.setStandardButtons(QMessageBox.Ok)
        error_box.exec_()