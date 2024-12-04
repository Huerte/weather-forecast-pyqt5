from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow
from PyQt5.QtCore import QPropertyAnimation, QRect, QEvent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Animated Button")
        self.setGeometry(100, 100, 400, 300)

        # Create a button
        self.button = QPushButton("Hover Me!", self)
        self.button.setGeometry(150, 120, 100, 40)

        # Install an event filter to detect hover events
        self.button.installEventFilter(self)

        # Create the animation object
        self.animation = QPropertyAnimation(self.button, b"geometry")
        self.animation.setDuration(100)  # Animation duration in milliseconds

    def eventFilter(self, obj, event):
        if obj == self.button:
            if event.type() == QEvent.Enter:  # Mouse hover starts
                self.animate_button(150, 150, 100, 50)  # Grow to new size
            elif event.type() == QEvent.Leave:  # Mouse hover ends
                self.animate_button(150, 140, 90, 40)  # Return to original size
        return super().eventFilter(obj, event)

    def animate_button(self, x, y, width, height):
        self.animation.stop()
        self.animation.setStartValue(self.button.geometry())
        self.animation.setEndValue(QRect(x, y, width, height))
        self.animation.start()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
'''
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGraphicsBlurEffect
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt


class BlurryWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the blur effect
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(5)  # Adjust the radius for more or less blur

        # Apply the blur effect to the widget
        self.setGraphicsEffect(blur_effect)

        # Set a semi-transparent background with white color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(255, 255, 255, 150))  # White with 150 alpha
        self.setPalette(palette)

        # Layout and example content
        layout = QVBoxLayout(self)
        label = QLabel(self)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QWidget()
    main_window.setWindowTitle("Blurry Transparent Widget with Background Image Example")

    # Apply a background image using a stylesheet
    main_window.setStyleSheet("""
        QWidget {
            background-image: url('assets/bg.jpg');  /* Replace with your image path */
            background-position: center;
            background-repeat: no-repeat;
            background-size: cover;
        }
    """)

    # Create the blurry widget
    main_layout = QVBoxLayout(main_window)
    blurry_widget = BlurryWidget()
    blurry_widget.setFixedSize(300, 200)

    main_layout.addWidget(blurry_widget)
    main_window.setLayout(main_layout)
    main_window.resize(400, 300)
    main_window.show()

    sys.exit(app.exec_())


'''


import requests

def get_location():
    response = requests.get("https://ipinfo.io/json")
    data = response.json()
    return {
        "city": data["city"],
        "loc": data["loc"],  # Latitude and longitude
    }
