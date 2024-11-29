from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox, QSizePolicy
from PyQt5.QtCore import Qt


class LoginWindow:
    def __init__(self, stack_widget):
        self.stack_widget = stack_widget
        self.name_input = ""
        self.password_input = ""

    def display(self):
        # Create the main window
        window = QWidget()
        window.setWindowTitle("Login Page")

        # Create a vertical layout for the window
        layout = QVBoxLayout()

        layout.addSpacing(20)

        # Create and configure the header
        header = QLabel("Login Account")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: white")
        layout.addWidget(header, alignment=Qt.AlignCenter)

        layout.addSpacing(20)

        # Create and configure the username input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your username")
        self.name_input.setStyleSheet("""
            QLineEdit {
                border-color: none;  /* Border color */
                border: 0.5px solid white;
                color: white;
                border-radius: 20px;      
                padding: 5px;            
                font-size: 15px;   
            }
        """)
        self.name_input.setFixedHeight(50)  # Standardize input height
        self.name_input.setFixedWidth(300)  # Standardize input width
        layout.addWidget(self.name_input, alignment=Qt.AlignCenter)

        layout.addSpacing(5)

        # Create and configure the password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setStyleSheet("""
            QLineEdit {
                border-color: none;
                border: 0.5px solid white;
                color: white;
                border-radius: 20px;
                padding: 5px;
                font-size: 15px; 
            }
        """)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(50)  # Standardize input height
        self.password_input.setFixedWidth(300)  # Standardize input width
        layout.addWidget(self.password_input, alignment=Qt.AlignCenter)

        layout.addSpacing(20)

        # Create and configure the login button
        login_button = QPushButton("Login")
        login_button.setFixedHeight(40)  # Standardize button height
        login_button.setFixedWidth(150)  # Standardize button width
        login_button.setStyleSheet("""
            font-size: 15px;
            border-radius: 20px; 
            background-color: #007BFF; 
            color: white;  
        """)
        login_button.clicked.connect(lambda: self.proceed_to_home_page(window))
        layout.addWidget(login_button, alignment=Qt.AlignCenter)

        layout.addSpacing(5)

        register_button = QPushButton("Create an account")
        register_button.setFixedHeight(40)  # Standardize button height
        register_button.setFixedWidth(150)  # Standardize button width
        register_button.setStyleSheet("border: none; font-size: 12px; color: white")

        register_button.clicked.connect(lambda: self.proceed_to_register_page())
        layout.addWidget(register_button, alignment=Qt.AlignCenter)

        # Set the layout to the main window and align contents to the center
        window.setLayout(layout)
        layout.setAlignment(Qt.AlignCenter)

        return window

    def proceed_to_home_page(self, window):
        if self.name_input.text().strip() == "" or self.password_input.text().strip() == "":
            self.show_error_message(window, "Hayap kaw Loy?", "Empty input field detected!")

        elif self.name_input.text() == "ako" and self.password_input.text() == "password":
            self.clear_input_fields()
            self.stack_widget.setCurrentIndex(2)
        else:
            self.show_error_message(window, "Error Loy", "User Does Not Exist!")
            self.clear_input_fields()

    def proceed_to_register_page(self):
        self.stack_widget.setCurrentIndex(1)

    def clear_input_fields(self):
        self.name_input.clear()
        self.password_input.clear()

    @staticmethod
    def show_error_message(window, title, message):
        error_box = QMessageBox(window)
        error_box.setIcon(QMessageBox.Critical)
        error_box.setStyleSheet("color: white;")
        error_box.setWindowTitle(title)
        error_box.setText(message)
        error_box.setStandardButtons(QMessageBox.Ok)
        error_box.exec_()