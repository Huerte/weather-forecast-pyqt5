#  KAYAOT SA IM NGAYAN CHARD
import pyqt5.QtWidgets as qtw
import sys


class MainWindow(qtw.QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Binoang na Window")
    self.setGeometry(100, 100, 500, 500)
    self.show()


def main():
  app = qtw.QApplication(sys.argv)
  window = MainWindow(app)
  window.show()
  sys.exit(app.exec_())


if __name__ == "__main__":
  main()