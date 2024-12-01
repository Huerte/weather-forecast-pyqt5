import sys
from PyQt5.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QWidget, QLabel


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the UI components
        self.setWindowTitle("PyQt5 Placeholder and Enter Example")
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout()

        self.label = QLabel("Type something and press Enter:")
        self.layout.addWidget(self.label)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter your text here...")  # Add placeholder
        self.layout.addWidget(self.input_field)

        # Connect Enter key to the method
        self.input_field.returnPressed.connect(self.on_enter_pressed)

        self.setLayout(self.layout)

    def on_enter_pressed(self):
        """This method is executed when the Enter key is pressed."""
        text = self.input_field.text()
        self.label.setText(f"You entered: {text}")
        self.input_field.clear()  # Optional: Clear the input field after Enter


# Main Application Execution
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
