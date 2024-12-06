from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox, QGridLayout
from PyQt5.QtCore import Qt
import sqlite3 as sql
import bcrypt #install bcrypt
from message_display import show_info_message, show_error_message



class RegisterWindow:
    def __init__(self, stack_widget):

        self.window = QWidget()
        self.stack_widget = stack_widget
        self.name_input = ""
        self.password_input, self.password2_input = "", ""

    def display(self):
        # Create a vertical layout for the main window
        layout = QVBoxLayout()

        # Create a background widget for the login window
        login_window = QWidget()
        login_window.setMinimumWidth(400)  # Allow resizing to a minimum width
        login_window.setMaximumHeight(700)  # Fixed height if desired
        login_window.setObjectName("register_window")
        login_window.setStyleSheet('''
            QWidget#register_window {
                background-color: rgba(255, 255, 255, 0.08);  /* Slightly opaque */
                border-radius: 30px;
                box-shadow: 1px 1px 50px rgba(0, 0, 0, 0.5);
            }
        ''')

        # Create a layout for the login window contents
        login_layout = QVBoxLayout()
        login_layout.setAlignment(Qt.AlignTop)  # Keep content at the top of the window

        login_layout.addSpacing(30)

        header = QLabel("Register Account")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: white")
        login_layout.addWidget(header, alignment=Qt.AlignCenter)

        login_layout.addSpacing(30)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        self.name_input.setFixedSize(300, 50)  # Fixed size for the input
        self.name_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid white;
                color: black;
                border-radius: 20px;
                padding: 5px;
                font-size: 15px;
                background-color: transparent;
            }
        """)
        login_layout.addWidget(self.name_input, alignment=Qt.AlignCenter)

        login_layout.addSpacing(5)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setFixedSize(300, 50)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid white;
                color: black;
                border-radius: 20px;
                padding: 5px;
                font-size: 15px;
                background-color: transparent;
            }
        """)
        login_layout.addWidget(self.password_input, alignment=Qt.AlignCenter)

        login_layout.addSpacing(5)

        self.password2_input = QLineEdit()
        self.password2_input.setPlaceholderText("Verify your password")
        self.password2_input.setFixedSize(300, 50)
        self.password2_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid white;
                color: black;
                border-radius: 20px;
                padding: 5px;
                font-size: 15px;
                background-color: transparent;
            }
        """)
        login_layout.addWidget(self.password2_input, alignment=Qt.AlignCenter)

        login_layout.addSpacing(20)

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
        register_button.clicked.connect(lambda: self.proceed_to_home_page())
        login_layout.addWidget(register_button, alignment=Qt.AlignCenter)

        login_layout.addSpacing(10)

        footer = QWidget()
        footer_layout = QGridLayout()
        label = QLabel("Already have an account?")
        label.setStyleSheet("font-size: 12px; color: white")
        login_button = QPushButton("Sign up")
        login_button.setFocusPolicy(Qt.NoFocus)
        login_button.setStyleSheet("border: none; color: #4757ff; font-size: 12px")
        login_button.clicked.connect(lambda: self.go_to_login_page())
        footer_layout.addWidget(label, 0, 0)
        footer_layout.addWidget(login_button, 0, 1)
        footer.setLayout(footer_layout)

        login_layout.addWidget(footer, alignment=Qt.AlignCenter)

        login_window.setLayout(login_layout)

        # Use stretch in the outer layout to allow the login window to center itself
        layout.addStretch()  # Push the content to center
        layout.addWidget(login_window, alignment=Qt.AlignCenter)
        layout.addStretch()  # Push the content to center

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