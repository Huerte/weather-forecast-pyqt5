from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt


class RegisterWindow:
    def __init__(self, stack_widget):
        self.stack_widget = stack_widget
        self.name_input = ""
        self.password_input, self.password2_input = "", ""

    def display(self):
        window = QWidget()
        layout = QVBoxLayout()

        header = QLabel("Register Account")
        layout.addWidget(header, alignment=Qt.AlignCenter | Qt.AlignBottom)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        layout.addWidget(self.name_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        layout.addWidget(self.password_input)

        self.password2_input = QLineEdit()
        self.password2_input.setPlaceholderText("Verify your password")
        layout.addWidget(self.password2_input)

        register_button = QPushButton("Register")
        register_button.clicked.connect(lambda: self.proceed_to_home_page(window))
        layout.addWidget(register_button)

        window.setLayout(layout)

        return window

    def proceed_to_home_page(self, window):
        if self.name_input.text().strip() == "" or self.password_input.text().strip() == "":
            self.show_error_message(window, "Hayap kaw Loy?", "Empty input field detected!")
        elif self.password_input.text() != self.password2_input.text():
            self.show_error_message(window, "Tarunga lagi ayay", "Password does not match!")
        else:
            self.stack_widget.setCurrentIndex(2)

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