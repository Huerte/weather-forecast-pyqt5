#  KAYAOT SA IM NGAYAN CHARD!!!
# MAS YAUT KAW RALD !!!
from distutils.command.register import register

import PyQt5.QtWidgets as qtw
import sys

from PyQt5.QtWidgets import QWidget, QLayout
from login import LoginWindow
from register import RegisterWindow


class MainWindow:
  def __init__(self):
    self.main_window = qtw.QMainWindow()
    self.main_window.setWindowTitle("Binoang na Window")
    self.main_window.setGeometry(100, 100, 500, 500)

    self.stack_widget = qtw.QStackedWidget()

    self.login_page = LoginWindow(self.stack_widget).display()
    self.register_page = RegisterWindow(self.stack_widget).display()
    self.stack_widget.addWidget(self.login_page)
    self.stack_widget.addWidget(self.register_page)

    self.main_window.setCentralWidget(self.stack_widget)

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

  def func(self):
    pass

def main():
  app = qtw.QApplication(sys.argv)
  window = MainWindow()
  sys.exit(app.exec_())


if __name__ == "__main__":
  main()