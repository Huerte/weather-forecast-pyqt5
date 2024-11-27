from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout


class LoginWindow:
    def __init__(self, stack_widget):
        self.stack_widget = stack_widget

    def display(self):
        window = QWidget()
        layout = QVBoxLayout()

        login_button = QPushButton("Login")
        login_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(1))
        layout.addWidget(login_button)

        window.setLayout(layout)

        return window