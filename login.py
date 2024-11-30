from PyQt5.QtWidgets import QWidget, QPushButton, \
    QVBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import Qt
import sqlite3 as sql
import bcrypt
from message_display import show_error_message


class LoginWindow:
    def __init__(self, stack_widget):
        self.window = None
        self.stack_widget = stack_widget
        self.name_input = ""
        self.password_input = ""

    def display(self):
        # Create the main selfwindow
        self.window = QWidget()
        self.window.setWindowTitle("Login Page")

        # Create a vertical layout for the selfwindow
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
        self.name_input.returnPressed.connect(self.proceed_to_home_page)
        layout.addWidget(self.name_input, alignment=Qt.AlignCenter)


        layout.addSpacing(5)

        # Create and configure the password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.returnPressed.connect(self.proceed_to_home_page)
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
        login_button.setFocusPolicy(Qt.NoFocus)
        login_button.setFixedHeight(40)  # Standardize button height
        login_button.setFixedWidth(150)  # Standardize button width
        login_button.setStyleSheet("""
            font-size: 15px;
            border-radius: 20px; 
            background-color: #007BFF; 
            color: white;  
        """)
        login_button.clicked.connect(lambda: self.proceed_to_home_page())
        layout.addWidget(login_button, alignment=Qt.AlignCenter)

        layout.addSpacing(5)

        register_button = QPushButton("Create an account")
        register_button.setFocusPolicy(Qt.NoFocus)
        register_button.setFixedHeight(40)  # Standardize button height
        register_button.setFixedWidth(150)  # Standardize button width
        register_button.setStyleSheet("border: none; font-size: 12px; color: white")

        register_button.clicked.connect(lambda: self.proceed_to_register_page())
        layout.addWidget(register_button, alignment=Qt.AlignCenter)

        # Set the layout to the main selfwindow and align contents to the center
        self.window.setLayout(layout)
        layout.setAlignment(Qt.AlignCenter)

        return self.window

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
            cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()

            if user:
                stored_hashed_password = user[0]
                if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                    print(f"Welcome back, {username}!")
                    self.stack_widget.setCurrentIndex(2)
                    return True
                else:
                    print("Invalid password!")
                    self.password_input.clear()
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

    