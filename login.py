from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit


class LoginWindow:
    def __init__(self, stack_widget):
        self.stack_widget = stack_widget

    def display(self):
        window = QWidget()
        layout = QVBoxLayout()

        header = QLabel("Login Account")
        layout.addWidget(header)

        name_input = QLineEdit()
        name_input.setPlaceholderText("Enter your username")
        layout.addWidget(name_input)

        password_input = QLineEdit()
        password_input.setPlaceholderText("Enter your password")
        layout.addWidget(password_input)

        login_button = QPushButton("Login")
        login_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(2))
        layout.addWidget(login_button)

        window.setLayout(layout)

        return window