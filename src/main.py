#  KAYAOT SA IM NGAYAN CHARD!!!
# MAS YAUT KAW RALD !!!

import sqlite3 as sql
import PyQt5.QtWidgets as qtw
import sys
from PyQt5.QtGui import QIcon
from auth.login import LoginWindow
from auth.register import RegisterWindow
from home import HomePage
from components.message_display import show_ask_message


class MainWindow:
    def __init__(self):
        self.home_page = None
        self.register_page = None
        self.login_page = None
        self.stack_widget = None
        self.main_window = None

        if self.create_database():
            self.setup_window()

    def setup_window(self):
        self.main_window = qtw.QMainWindow()
        self.main_window.setWindowTitle("Nimbus")

        self.main_window.setWindowIcon(QIcon("assets/icons/logo.png"))

        # Set backgrounds image and text color
        self.main_window.setStyleSheet("""
          QMainWindow {
              background-image: url('assets/background/default.jpg'); 
              background-position: center;
              background-repeat: no-repeat;
              color: white;
          }
        """) 

        WIDTH, HEIGHT = 1080, 600
        self.main_window.resize(WIDTH, HEIGHT)

        self.main_window.setMinimumSize(1080, 600)

        self.stack_widget = qtw.QStackedWidget()
        login = LoginWindow(self.stack_widget)
        self.home_page = HomePage(self.main_window, self.stack_widget, login.loading).display()
        self.login_page = login.display()
        self.register_page = RegisterWindow(self.stack_widget).display()

        # Amo ini an pagkasunod nan mga window, index zero an una mo
        # respawn na page pag run ng program
        self.stack_widget.addWidget(self.login_page)  # index 0
        self.stack_widget.addWidget(self.register_page)  # index 1
        self.stack_widget.addWidget(self.home_page)  # index 2

        self.main_window.setCentralWidget(self.stack_widget)
        self.main_window.closeEvent = self.confirm_exit
        self.center_window()
        self.main_window.show()

    def center_window(self):
        # Get the geometry of the main window
        window_geometry = self.main_window.frameGeometry()

        # Get the center point of the screen
        screen_center = qtw.QDesktopWidget().availableGeometry().center()

        # Move the window's top-left point to the correct position
        window_geometry.moveCenter(screen_center)
        self.main_window.move(window_geometry.topLeft())

    @staticmethod
    def create_database():
        database_path = "database/user_accounts.db"
        conn = sql.connect(database_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Commit the transaction and close the connection
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            cursor.close()
            conn.close()

    def confirm_exit(self, event):
        """Show confirmation dialog when the application is about to quit."""
        reply = show_ask_message(self.main_window, "Confirm Exit", "Are you sure you want to exit?")
        if reply:
            sys.exit()
        else:
            event.ignore()


def main():
    app = qtw.QApplication(sys.argv)
    root = MainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
