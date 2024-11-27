#  KAYAOT SA IM NGAYAN CHARD!!!
# MAS YAUT KAW RALD !!!
import PyQt5.QtWidgets as qtw
import sys


class MainWindow(qtw.QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Binoang na Window")
    self.setGeometry(100, 100, 500, 500)
    self.show()
    self.centerWindow()

  def centerWindow(self):
    # Get the geometry of the main window
    window_geometry = self.frameGeometry()

    # Get the center point of the screen
    screen_center = qtw.QDesktopWidget().availableGeometry().center()

    # Move the window's top-left point to the correct position
    window_geometry.moveCenter(screen_center)
    self.move(window_geometry.topLeft())

  def func(self):
    pass

def main():
  app = qtw.QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec_())


if __name__ == "__main__":
  main()