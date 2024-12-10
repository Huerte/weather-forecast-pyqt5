import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt


class App:
    def __init__(self):
        # Create the main window instance
        self.main_window = QMainWindow()
        self.main_window.setWindowTitle("Scalable Font Example")
        self.main_window.resize(800, 600)

        # Central widget and layout
        self.central_widget = QWidget()
        self.main_window.setCentralWidget(self.central_widget)

        # Create a layout and add widgets
        self.layout = QVBoxLayout(self.central_widget)

        self.label = QLabel("This is a scalable label!")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.sub_label = QLabel("Resize the window to see the font scale.")
        self.sub_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.sub_label)

        # Adjust the font sizes initially
        self.adjust_fonts_and_sizes()

        # Connect the resize event
        self.main_window.resizeEvent = self.resize_event

    def adjust_fonts_and_sizes(self):
        # Get current window size
        width = self.main_window.size().width()
        height = self.main_window.size().height()

        # Calculate a font size proportional to window size
        font_size = int(min(width, height) * 0.05)  # 5% of the smaller dimension

        # Apply font size to all labels
        for widget in [self.label, self.sub_label]:
            font = widget.font()
            font.setPointSize(font_size)
            widget.setFont(font)

    def resize_event(self, event):
        # Adjust fonts and sizes when the window is resized
        self.adjust_fonts_and_sizes()

        # Call the original QMainWindow resize event
        QMainWindow.resizeEvent(self.main_window, event)

    def show(self):
        # Show the main window
        self.main_window.show()


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    application = App()
    application.show()
    sys.exit(app.exec_())
