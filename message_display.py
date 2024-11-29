from PyQt5.QtWidgets import QMessageBox


def show_error_message(window, title, message):
    error_box = QMessageBox(window)
    error_box.setIcon(QMessageBox.Critical)
    error_box.setStyleSheet("color: white")
    error_box.setWindowTitle(title)
    error_box.setText(message)
    error_box.setStandardButtons(QMessageBox.Ok)
    error_box.exec_()


def show_info_message(window, title, message):
    error_box = QMessageBox(window)
    error_box.setIcon(QMessageBox.Information)
    error_box.setStyleSheet("color: white")
    error_box.setWindowTitle(title)
    error_box.setText(message)
    error_box.setStandardButtons(QMessageBox.Ok)
    error_box.exec_()