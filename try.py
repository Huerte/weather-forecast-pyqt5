###
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
