from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox, QGridLayout
from PyQt5.QtCore import Qt
import sqlite3 as sql
import bcrypt #install bcrypt
from components.message_display import show_info_message, show_error_message



class RegisterWindow:
    def __init__(self, stack_widget):

        self.window = QWidget()
        self.stack_widget = stack_widget
        self.name_input = ""
        self.password_input, self.password2_input = "", ""
        self.font_size = 30

    def display(self):
        # Create a vertical layout for the main window
        layout = QVBoxLayout()

        layout.addSpacing(30)

        header = QLabel("Register Account")
        header.setStyleSheet(f"color: white")
        header.setFont(QFont("Arial", self.font_size-5))
        layout.addWidget(header, alignment=Qt.AlignCenter)

        layout.addSpacing(30)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        self.name_input.setFixedSize(300, 50)  # Fixed size for the input
        self.name_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid white;
                color: black;
                border-radius: 20px;
                padding: 5px;
            }
        """)
        self.name_input.setFont(QFont("Arial", self.font_size-20))
        layout.addWidget(self.name_input, alignment=Qt.AlignCenter)

        layout.addSpacing(5)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setFixedSize(300, 50)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid white;
                color: black;
                border-radius: 20px;
                padding: 5px;
            }
        """)
        self.password_input.setFont(QFont("Arial", self.font_size-20))
        layout.addWidget(self.password_input, alignment=Qt.AlignCenter)

        layout.addSpacing(5)

        self.password2_input = QLineEdit()
        self.password2_input.setPlaceholderText("Verify your password")
        self.password2_input.setFixedSize(300, 50)
        self.password2_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid white;
                color: black;
                border-radius: 20px;
                padding: 5px;
            }
        """)
        self.password2_input.setFont(QFont("Arial", self.font_size-20))
        layout.addWidget(self.password2_input, alignment=Qt.AlignCenter)

        layout.addSpacing(20)

        register_button = QPushButton("Register")
        register_button.setFixedSize(150, 40)
        register_button.setStyleSheet("""
            QPushButton {
                font-size: 15px;
                border-radius: 20px;
                background-color: #007BFF;
                color: white;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        register_button.setFont(QFont("Arial", self.font_size - 25))
        register_button.clicked.connect(lambda: self.proceed_to_home_page())
        layout.addWidget(register_button, alignment=Qt.AlignCenter)

        layout.addSpacing(10)

        footer = QWidget()
        footer_layout = QGridLayout()
        label = QLabel("Already have an account?")
        label.setStyleSheet("color: white")
        label.setFont(QFont("Arial", self.font_size-20))
        login_button = QPushButton("Sign up")
        login_button.setFocusPolicy(Qt.NoFocus)
        login_button.setStyleSheet("border: none; color: #4757ff;")
        login_button.clicked.connect(lambda: self.go_to_login_page())
        login_button.setFont(QFont("Arial", self.font_size-20))
        footer_layout.addWidget(label, 0, 0)
        footer_layout.addWidget(login_button, 0, 1)
        footer.setLayout(footer_layout)

        layout.addWidget(footer, alignment=Qt.AlignCenter)

        self.window.setLayout(layout)
        layout.setAlignment(Qt.AlignCenter)

        return self.window

    def proceed_to_home_page(self):
        if not self.name_input.text().strip():
            show_error_message(self.window, "Empty Fields", "Username cannot be empty.")
            return
        if len(self.password_input.text()) < 8:
            show_error_message(self.window, "Weak Password", "Password must be at least 8 characters.")
            return
        if self.password_input.text() != self.password2_input.text():
            show_error_message(self.window, "Password Mismatch", "Passwords do not match!")
            return
        self.register_account(self.name_input.text().strip(), self.password_input.text().strip())

    def register_account(self, username, password):
        database_path = "database/user_accounts.db"
        conn = sql.connect(database_path)
        cursor = conn.cursor()

        cursor.execute('SELECT username, password FROM users')
        users = cursor.fetchall()

        if self.hash_search(users, username):
            show_error_message(self.window, "Kausik naunhan nakaw!", "1Username already exists!")
            return

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
            self.stack_widget.setCurrentIndex(0) #Mobalik ini sa login page
        except sql.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                show_error_message(self.window, "Kausik naunhan nakaw!", "Username already exists!")
            else:
                print("Error:", e)
        finally:
            cursor.close()
            conn.close()

    def go_to_login_page(self):
        self.clear_input_fields()
        self.stack_widget.setCurrentIndex(0)

    def clear_input_fields(self):
        self.name_input.clear()
        self.password_input.clear()
        self.password2_input.clear()

    @staticmethod
    def hash_search(arr, username):
        user_dictionary = {user[0]: user[1] for user in arr}
        if username in user_dictionary:
            return True
        else:
            return False