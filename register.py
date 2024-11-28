from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit


class RegisterWindow:
    def __init__(self, stack_widget):
        self.stack_widget = stack_widget

    def display(self):
        window = QWidget()
        layout = QVBoxLayout()

        header = QLabel("Register Account")
        layout.addWidget(header)

        name_input = QLineEdit()
        name_input.setPlaceholderText("Enter your name")
        layout.addWidget(name_input)

        password_input = QLineEdit()
        password_input.setPlaceholderText("Enter your password")
        layout.addWidget(password_input)

        password2_input = QLineEdit()
        password2_input.setPlaceholderText("Verify your password")
        layout.addWidget(password2_input)

        register_button = QPushButton("Register")
        register_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(2))
        layout.addWidget(register_button)

        window.setLayout(layout)

        return window