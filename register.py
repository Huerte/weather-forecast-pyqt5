from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout


class RegisterWindow:
    def __init__(self, stack_widget):
        self.stack_widget = stack_widget

    def display(self):
        window = QWidget()
        layout = QVBoxLayout()

        register_button = QPushButton("Register")
        register_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(2))
        layout.addWidget(register_button)

        window.setLayout(layout)

        return window