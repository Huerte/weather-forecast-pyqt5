import sys
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QRegion, QFont
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsBlurEffect, QStackedLayout
)


class BlurredBackgroundWidget(QWidget):
    def __init__(self, parent=None, blur_radius=15):
        super().__init__(parent)
        self.blur_radius = blur_radius
        self.setAttribute(Qt.WA_TranslucentBackground)  # Enable transparency
        self.setStyleSheet("background: transparent;")  # Transparent background for the widget

        # Main layout for stacking blurred background and sharp content
        self.stacked_layout = QStackedLayout(self)
        self.stacked_layout.setStackingMode(QStackedLayout.StackAll)

        # Label to display the blurred background
        self.blur_label = QLabel(self)
        self.blur_label.setStyleSheet("background: transparent;")
        self.stacked_layout.addWidget(self.blur_label)

        # Widget for the sharp content
        self.content_widget = QWidget(self)
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(10, 10, 10, 10)  # Margins for content
        self.stacked_layout.addWidget(self.content_widget)

    def add_content(self, widget):
        """Add a widget to the content layer."""
        self.content_layout.addWidget(widget)

    def blur_background(self):
        """Capture and blur the background."""
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.transparent)

        # Render the widget's background into the pixmap
        painter = QPainter(pixmap)
        self.render(painter, QPoint(), QRegion(self.rect()), renderFlags=QPainter.OpaqueHint)
        painter.end()

        # Apply the blur effect
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(self.blur_radius)
        self.blur_label.setPixmap(pixmap)
        self.blur_label.setGraphicsEffect(blur_effect)


class ExampleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blurred Background Example")
        self.setStyleSheet("background-color: rgba(255, 255, 255, 1);")  # Full opaque window background

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create a blurred background widget
        self.top_section = BlurredBackgroundWidget(blur_radius=15)
        self.top_section.setFixedHeight(200)  # Fixed height for the demo
        main_layout.addWidget(self.top_section)

        # Add content to the blurred section
        date_label = QLabel("Today, December 5")
        date_label.setFont(QFont("Arial", 15))
        self.top_section.add_content(date_label)

        city_label = QLabel("Sample City, Country")
        city_label.setFont(QFont("Arial", 20))
        self.top_section.add_content(city_label)

        temperature_label = QLabel("25°C, Sunny")
        temperature_label.setFont(QFont("Arial", 30))
        self.top_section.add_content(temperature_label)

        # Trigger the blur effect once the layout is set
        self.top_section.blur_background()

        # Placeholder for the main content below
        placeholder_label = QLabel("Other window content...")
        placeholder_label.setFont(QFont("Arial", 15))
        main_layout.addWidget(placeholder_label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExampleApp()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())

'''
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
'''
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGraphicsBlurEffect
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt




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
