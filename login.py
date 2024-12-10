from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, \
    QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QSizePolicy, QGridLayout
from PyQt5.QtCore import Qt, QSize
import sqlite3 as sql
import bcrypt
from message_display import show_error_message
from Loading import LoadingOverlay
from icon_color_changer import change_icon_color


class LoginWindow:
    def __init__(self, stack_widget):
        self.visible_btn = None
        self.window = self.window = QWidget()
        self.window.setWindowTitle("Login Page")

        self.stack_widget = stack_widget
        self.name_input = ""
        self.password_input = ""
        self.loading = LoadingOverlay(self.window)
        self.font_size = 30
        self.btn_color = "black"
        self.password_visible = False

    def display(self):
        layout = QVBoxLayout()

        layout.addSpacing(20)

        # Create and configure the header
        header = QLabel("Login Account")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet(f"color: white")
        header.setFont(QFont("Arial", self.font_size-5))
        layout.addWidget(header, alignment=Qt.AlignCenter)

        layout.addSpacing(40)

        # Create and configure the username input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your username")
        self.name_input.setStyleSheet(f"border: 0.5px solid white; color: black; border-radius: 20px; padding: 0px 10px;")
        self.name_input.setFont(QFont("Arial", self.font_size - 20))
        self.name_input.setFixedHeight(50)  # Standardize input height
        self.name_input.setFixedWidth(300)  # Standardize input width
        self.name_input.returnPressed.connect(self.proceed_to_home_page)
        layout.addWidget(self.name_input, alignment=Qt.AlignCenter)

        layout.addSpacing(5)

        # Create and configure the password input
        password_section = QWidget()
        password_section.setFixedHeight(50)
        password_section.setFixedWidth(300)
        password_section.setStyleSheet("""
                border: 0.5px solid white;
                border-radius: 20px;
                background-color: white;
        """)
        password_layout = QGridLayout()

        self.password_input = QLineEdit()
        self.password_input.setMinimumWidth(280)
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.returnPressed.connect(self.proceed_to_home_page)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: none;
                color: black;
                background-color: transparent;
            }
        """)
        self.password_input.setFont(QFont("Arial", self.font_size - 20))
        self.password_input.setEchoMode(QLineEdit.Password)

        self.visible_btn = QPushButton()

        self.visible_btn.setIconSize(QSize(25, 25))
        self.visible_btn.setFixedSize(30, 30)
        self.visible_btn.setFocusPolicy(Qt.NoFocus)
        self.visible_btn.setStyleSheet('''
            QPushButton {
                font-size: 15px;
                border: none;
                margin: none;
            }
            QPushButton:hover {
                opacity: 0.8;
            }
        ''')
        self.visible_btn.setIcon(QIcon("assets/icons/visible_off.png"))
        change_icon_color(self.visible_btn, "assets/icons/visible_off.png", self.btn_color)
        self.visible_btn.clicked.connect(self.show_hide_password)
        password_layout.addWidget(self.password_input, 0, 0, alignment=Qt.AlignLeft)
        password_layout.addWidget(self.visible_btn, 0, 1, alignment=Qt.AlignRight)
        password_section.setLayout(password_layout)

        layout.addWidget(password_section, alignment=Qt.AlignCenter)

        layout.addSpacing(20)

        # Create and configure the login button
        login_button = QPushButton("Login")
        login_button.setFocusPolicy(Qt.NoFocus)
        login_button.setFixedHeight(40)  # Standardize button height
        login_button.setFixedWidth(160)  # Standardize button width
        login_button.setStyleSheet("""
            border-radius: 20px; 
            background-color: #007BFF; 
            color: white;  
        """)
        login_button.setFont(QFont("Arial", self.font_size - 20))
        login_button.clicked.connect(lambda: self.proceed_to_home_page())
        layout.addWidget(login_button, alignment=Qt.AlignCenter)

        layout.addSpacing(5)

        register_button = QPushButton("Create an account")
        register_button.setFocusPolicy(Qt.NoFocus)
        register_button.setStyleSheet("border: none; color: white")
        register_button.setFont(QFont("Arial", self.font_size - 20))

        register_button.clicked.connect(lambda: self.proceed_to_register_page())
        layout.addWidget(register_button, alignment=Qt.AlignCenter)

        # Set the layout to the main self window and align contents to the center
        self.window.setLayout(layout)
        layout.setAlignment(Qt.AlignCenter)

        return self.window

    def show_hide_password(self):
        if not self.password_visible:
            change_icon_color(self.visible_btn, "assets/icons/visible_on.png", self.btn_color)
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            change_icon_color(self.visible_btn, "assets/icons/visible_off.png", self.btn_color)
            self.password_input.setEchoMode(QLineEdit.Password)

        self.password_visible = not self.password_visible

    def proceed_to_home_page(self):
        if self.name_input.text().strip() == "" or self.password_input.text().strip() == "":
            show_error_message(self.window, "Hayap kaw Loy?", "Empty input field detected!")
        elif self.login_account(self.name_input.text(), self.password_input.text().strip()):
            self.clear_input_fields()

    def login_account(self, username, password):
        database_path = "auth/user_accounts.db"
        conn = sql.connect(database_path)
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT username, password FROM users')
            users = cursor.fetchall()

            stored_password = self.linear_search(users, username)

            if stored_password:
                if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                    print(f"Welcome back, {username}!")


                    self.stack_widget.setCurrentIndex(2)

                    return True
                else:
                    show_error_message(self.window, "Account does not exists!", "Invalid username or password")
                    self.clear_input_fields()
                    return False
            else:
                show_error_message(self.window, "Account does not exists!", "Invalid username or password")
                self.clear_input_fields()
                return False

        except Exception as e:
            print(f"{e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def clear_input_fields(self):
        self.name_input.clear()
        self.password_input.clear()

    def proceed_to_register_page(self):
        self.stack_widget.setCurrentIndex(1)

    @staticmethod
    def linear_search(arr, username):
        for (name, password) in arr:
            if name == username:
                return password
        return None