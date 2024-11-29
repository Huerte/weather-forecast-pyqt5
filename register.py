from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox, QGridLayout
from PyQt5.QtCore import Qt


class RegisterWindow:
    def __init__(self, stack_widget):
        self.stack_widget = stack_widget
        self.name_input = ""
        self.password_input, self.password2_input = "", ""

    def display(self):
        window = QWidget()

        # Create a vertical layout for the window
        layout = QVBoxLayout()

        layout.addSpacing(20)

        header = QLabel("Register Account")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: white")
        layout.addWidget(header, alignment=Qt.AlignCenter)

        layout.addSpacing(20)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        #self.name_input.setStyleSheet("font-size: 15px; color: white")
        self.name_input.setStyleSheet("""
            QLineEdit {
                border-color: none;
                border: 0.5px solid white;
                color: white;
                border-radius: 20px;
                padding: 5px;
                font-size: 15px;
            }
        """)
        self.name_input.setFixedHeight(50)  # Standardize input height
        self.name_input.setFixedWidth(300)  # Standardize input width
        layout.addWidget(self.name_input)

        layout.addSpacing(5)

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
        self.password_input.setFixedHeight(50)  # Standardize input height
        self.password_input.setFixedWidth(300)  # Standardize input width
        layout.addWidget(self.password_input)

        layout.addSpacing(5)

        self.password2_input = QLineEdit()
        self.password2_input.setPlaceholderText("Verify your password")
        self.password2_input.setStyleSheet("""
            QLineEdit {
                border-color: none;  /* Border color */
                border: 0.5px solid white;
                color: white;
                border-radius: 20px;   
                padding: 5px;         
                font-size: 15px;
            }
        """)
        self.password2_input.setFixedHeight(50)  # Standardize input height
        self.password2_input.setFixedWidth(300)  # Standardize input width
        layout.addWidget(self.password2_input)

        layout.addSpacing(20)

        register_button = QPushButton("Register")
        register_button.setFixedHeight(40)  # Standardize button height
        register_button.setFixedWidth(150)  # Standardize button width
        register_button.setStyleSheet("""
                    font-size: 15px;
                    border-radius: 20px;
                    background-color: #007BFF;
                    color: white;
                """)
        register_button.clicked.connect(lambda: self.proceed_to_home_page(window))
        layout.addWidget(register_button, alignment=Qt.AlignCenter)

        layout.addSpacing(5)

        footer = QWidget()
        layout2 = QGridLayout()
        layout2.setContentsMargins(0, 0, 0, 0)
        layout2.setSpacing(0)

        # Create and configure the label
        label = QLabel("Already had an Account?")
        label.setStyleSheet("margin-right: 0px; font-size: 12px; color: white")
        layout2.addWidget(label, 0, 0)

        # Create and configure the sign-up button
        login_button = QPushButton("Sign up")
        login_button.setFixedHeight(40)  # Standardize button height
        login_button.setStyleSheet("border: none; color: #4757ff; font-size: 12px")
        login_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(0))
        layout2.addWidget(login_button, 0, 1)

        # Set the layout to the footer widget
        footer.setLayout(layout2)

        # Add the footer to the main layout
        layout.addWidget(footer)

        window.setLayout(layout)
        layout.setAlignment(Qt.AlignCenter)

        return window

    def proceed_to_home_page(self, window):
        if self.name_input.text().strip() == "" or self.password_input.text().strip() == "":
            self.show_error_message(window, "Hayap kaw Loy?", "Empty input field detected!")
        elif self.password_input.text() != self.password2_input.text():
            self.show_error_message(window, "Tarunga lagi ayay laman!", "Password does not match!")
        else:
            self.clear_input_fields()
            self.stack_widget.setCurrentIndex(0)

    def clear_input_fields(self):
        self.name_input.clear()
        self.password_input.clear()

    @staticmethod
    def show_error_message(window, title, message):
        error_box = QMessageBox(window)
        error_box.setIcon(QMessageBox.Critical)
        error_box.setStyleSheet("color: white")
        error_box.setWindowTitle(title)
        error_box.setText(message)
        error_box.setStandardButtons(QMessageBox.Ok)
        error_box.exec_()