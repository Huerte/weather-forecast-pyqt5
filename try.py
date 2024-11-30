import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit
)
from PyQt5.QtCore import Qt, QEvent, QSize
from PyQt5.QtGui import QIcon

class HomePage(QWidget):
    def __init__(self, stack_widget: QStackedWidget):
        super().__init__()
        self.menu_panel = None
        self.menu_btn = None
        self.MENU_PANEL_WIDTH = 200
        self.stack_widget = stack_widget

    def display(self):
        self.home_page = QWidget()
        self.main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()

        # Menu Button
        self.menu_btn = QPushButton()
        self.menu_btn.setIcon(QIcon("assets/icons/menu.png"))  # Ensure the icon path exists or replace with another icon.
        self.menu_btn.setIconSize(QSize(30, 30))
        self.menu_btn.clicked.connect(self.open_menu)

        # Menu Panel
        self.menu_panel = QWidget(self.home_page)
        self.menu_panel.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.menu_panel.setGeometry(0, 0, self.MENU_PANEL_WIDTH, 300)
        self.menu_panel.setStyleSheet("background-color: rgba(0, 0, 0, 0.23); border-radius: 5px;")
        self.menu_panel.hide()

        # Install Event Filter on self.home_page
        self.home_page.installEventFilter(self)

        # Layout setup
        top_layout.addWidget(self.menu_btn, alignment=Qt.AlignLeft)
        self.main_layout.addLayout(top_layout)
        self.home_page.setLayout(self.main_layout)

        return self.home_page

    def open_menu(self):
        if self.menu_panel.isVisible():
            self.menu_panel.hide()
        else:
            self.menu_panel.show()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress and self.menu_panel.isVisible():
            print("Mouse pressed detected!")
            if not self.menu_panel.geometry().contains(event.globalPos()):
                print("Closing menu due to outside click")
                self.menu_panel.hide()
        return super().eventFilter(obj, event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home Page with Menu")
        self.setGeometry(100, 100, 800, 600)

        # Create a QStackedWidget
        self.stack_widget = QStackedWidget()

        # Add HomePage to QStackedWidget
        self.home_page = HomePage(self.stack_widget)
        self.stack_widget.addWidget(self.home_page.display())

        # Set central widget
        self.setCentralWidget(self.stack_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
