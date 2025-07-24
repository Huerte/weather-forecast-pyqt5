from PyQt5.QtWidgets import QMessageBox


def show_error_message(window, title, message):
    error_box = QMessageBox(window)
    error_box.setIcon(QMessageBox.Critical)
    error_box.setStyleSheet("color: black")
    error_box.setWindowTitle(title)
    error_box.setText(message)
    error_box.setStandardButtons(QMessageBox.Ok)
    error_box.exec_()


def show_info_message(window, title, message):
    info_box = QMessageBox(window)
    info_box.setIcon(QMessageBox.Information)
    info_box.setStyleSheet("color: black")
    info_box.setWindowTitle(title)
    info_box.setText(message)
    info_box.setStandardButtons(QMessageBox.Ok)
    info_box.exec_()

def show_ask_message(window, title, message):
    ask_box = QMessageBox(window)
    ask_box.setIcon(QMessageBox.Question)
    ask_box.setStyleSheet("color: black")
    ask_box.setWindowTitle(title)
    ask_box.setText(message)
    ask_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    ask_box.setDefaultButton(QMessageBox.No)  # Highlight "No" as the default option

    response = ask_box.exec_()
    return response == QMessageBox.Yes