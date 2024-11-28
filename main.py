#  KAYAOT SA IM NGAYAN CHARD!!!
# MAS YAUT KAW RALD !!!

import PyQt5.QtWidgets as qtw
from PyQt5.QtCore import Qt
import sys
from login import LoginWindow
from register import RegisterWindow


class MainWindow:
  def __init__(self):
    self.main_window = qtw.QMainWindow()
    self.main_window.setWindowTitle("Binoang na Window")
    self.main_window.setStyleSheet(f"background-color: #131621;")
    size = 800
    self.main_window.setGeometry(size, size, 400, 400)


    self.stack_widget = qtw.QStackedWidget()

    self.login_page = LoginWindow(self.stack_widget).display()
    self.register_page = RegisterWindow(self.stack_widget).display()

    # Amo ini an pagkasunod nan mga window, index zero an una mo
    # respawn na page pag run ng program
    self.stack_widget.addWidget(self.login_page)  #index 0
    self.stack_widget.addWidget(self.register_page)  #index 1
    self.stack_widget.addWidget(self.display_home_page())  #index 2

    self.main_window.setCentralWidget(self.stack_widget)

    self.center_window()
    self.main_window.show()


  def display_home_page(self):
    home_page = qtw.QWidget()
    layout = qtw.QVBoxLayout()

    label = qtw.QLabel("Home Page")
    label.setStyleSheet("color: white;")
    layout.addWidget(label, alignment=Qt.AlignCenter)
    home_page.setLayout(layout)

    return home_page

  def center_window(self):
    # Get the geometry of the main window
    window_geometry = self.main_window.frameGeometry()

    # Get the center point of the screen
    screen_center = qtw.QDesktopWidget().availableGeometry().center()

    # Move the window's top-left point to the correct position
    window_geometry.moveCenter(screen_center)
    self.main_window.move(window_geometry.topLeft())

  def func(self):
    pass

def main():
  app = qtw.QApplication(sys.argv)
  window = MainWindow()
  sys.exit(app.exec_())


if __name__ == "__main__":
  main()