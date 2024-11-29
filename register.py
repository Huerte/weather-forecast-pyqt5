from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox, QGridLayout
from PyQt5.QtCore import Qt
import sqlite3 as sql
import bcrypt #install bcrypt
from message_display import show_info_message, show_error_message



class RegisterWindow:
    def __init__(self, stack_widget):
        self.stack_widget = stack_widget
        self.name_input = ""
        self.password_input, self.password2_input = "", ""

    def display(self):
        self.window = QWidget()

        # Create a vertical layout for the self.window
        layout = QVBoxLayout()

        layout.addSpacing(20)

        header = QLabel("Register Account")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: white")
        layout.addWidget(header, alignment=Qt.AlignCenter)

        layout.addSpacing(20)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
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
        register_button.clicked.connect(lambda: self.proceed_to_home_page())
        layout.addWidget(register_button, alignment=Qt.AlignCenter)

        layout.addSpacing(5)

        footer = QWidget()
        footer.setFixedWidth(210)
        layout2 = QGridLayout()

        # Create and configure the label
        label = QLabel("Already had an Account?")
        label.setStyleSheet("margin-right: 0px; font-size: 12px; color: white")
        layout2.addWidget(label, 0, 0)

        # Create and configure the sign-up button
        login_button = QPushButton("Sign up")
        login_button.setStyleSheet("border: none; color: #4757ff; font-size: 12px")
        login_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(0))
        layout2.addWidget(login_button, 0, 1)

        # Set the layout to the footer widget
        footer.setLayout(layout2)

        # Add the footer to the main layout
        layout.addWidget(footer, alignment=Qt.AlignCenter)

        self.window.setLayout(layout)
        layout.setAlignment(Qt.AlignCenter)

        return self.window

    def proceed_to_home_page(self):
        if self.name_input.text().strip() == "" or self.password_input.text().strip() == "":
            show_error_message(self.window, "Hayap kaw Loy?", "Empty input field detected!")
        elif self.password_input.text() != self.password2_input.text():
            show_error_message(self.window, "Tarunga lagi ayay laman!", "Password does not match!")
        else:
            self.register_account(self.name_input.text(), self.password_input.text())

    def register_account(self, username, password):
        database_path = "auth/user_accounts.db"
        conn = sql.connect(database_path)
        cursor = conn.cursor()

        # Hash password and decode to store as text in SQLite
        hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        try:
            cursor.execute('''
            INSERT INTO users (username, password)
            VALUES (?, ?)
            ''', (username, hash_password))
            conn.commit()
            show_info_message(self.window, "Hoy!", "User account\nsuccessfully created!")
            self.clear_input_fields()
            self.stack_widget.setCurrentIndex(0)
        except sql.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                show_error_message(self.window, "Kausik naunhan nakaw!", "Username already exists!")
            else:
                print("Error:", e)
        finally:
            cursor.close()
            conn.close()

    def clear_input_fields(self):
        self.name_input.clear()
        self.password_input.clear()
        self.password2_input.clear()