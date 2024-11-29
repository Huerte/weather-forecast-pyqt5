import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMenu, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle('Button Click to Show Menu')
        self.setGeometry(100, 100, 400, 300)

        # Create a central widget and layout
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        # Create a button
        button = QPushButton('Click Me to Show Menu', self)

        # Add the button to the layout
        layout.addWidget(button)

        # Connect the button click event to show the menu
        button.clicked.connect(self.show_menu)

        # Set the central widget
        self.setCentralWidget(central_widget)

    def show_menu(self):
        # Create a QMenu
        menu = QMenu(self)

        # Add actions to the menu
        action1 = menu.addAction('Open')
        action2 = menu.addAction('Save')
        action3 = menu.addAction('Exit')

        # Connect the actions to corresponding methods
        action1.triggered.connect(self.open_file)
        action2.triggered.connect(self.save_file)
        action3.triggered.connect(self.close)

        # Show the menu at the position of the button
        menu.exec_(self.mapToGlobal(self.sender().pos()))

    def open_file(self):
        print("Open selected")

    def save_file(self):
        print("Save selected")


# Create the application
app = QApplication(sys.argv)

# Create the main window
window = MainWindow()
window.show()

# Run the application
sys.exit(app.exec_())
