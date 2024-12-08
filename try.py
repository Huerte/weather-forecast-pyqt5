class Try:
    def categorize_weather_and_set_background(data):
        # Extract the main weather condition and description from the API response
        weather_main = data['weather'][0]['main'].lower()  # Example: "Rain", "Clear", "Snow"
        weather_description = data['weather'][0]['description'].lower()  # Detailed description (e.g. "light rain")

        # Generalize weather conditions into categories
        if weather_main in ['rain', 'drizzle', 'thunderstorm', 'tornado']:
            weather_category = "rainy"
            weather_details = f"Rainy weather ({weather_description})"
        elif weather_main in ['clear']:
            weather_category = "sunny"
            weather_details = f"Clear sky ({weather_description})"
        elif weather_main in ['snow']:
            weather_category = "snowy"
            weather_details = f"Snowy weather ({weather_description})"
        elif weather_main in ['clouds']:
            if 'few' in weather_description:
                weather_category = "sunny"  # Can categorize few clouds as sunny
                weather_details = f"Partly cloudy ({weather_description})"
            elif 'scattered' in weather_description:
                weather_category = "sunny"
                weather_details = f"Scattered clouds ({weather_description})"
            else:
                weather_category = "cloudy"
                weather_details = f"Overcast ({weather_description})"
        elif weather_main in ['fog', 'mist']:
            weather_category = "foggy"
            weather_details = f"Foggy or misty conditions ({weather_description})"
        elif weather_main in ['extreme']:
            weather_category = "extreme"
            weather_details = f"Extreme conditions ({weather_description})"
        else:
            weather_category = "other"
            weather_details = f"Other conditions ({weather_description})"

        # Map weather categories to backgrounds images
        background_images = {
            "rainy": "assets/backgrounds/rainy.jpg",
            "sunny": "assets/backgrounds/sunny.jpg",
            "snowy": "assets/backgrounds/snowy.jpg",
            "cloudy": "assets/backgrounds/cloudy.jpg",
            "foggy": "assets/backgrounds/foggy.jpg",
            "extreme": "assets/backgrounds/extreme.jpg",
            "other": "assets/backgrounds/default.jpg"
        }

        # Get the backgrounds image for the current weather category
        background_image = background_images.get(weather_category, "assets/backgrounds/default.jpg")

        # Set the backgrounds dynamically using PyQt (assuming you are setting the backgrounds of the main window or widget)
        self.setStyleSheet(f"QWidget {{ backgrounds-image: url({background_image}); }}")

        # You can also use the weather_details variable to display more detailed information on your UI
        print(f"Weather is categorized as: {weather_category}")
        print(f"Weather details: {weather_details}")

        return weather_category, weather_details

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
    main_window.setWindowTitle("Blurry Transparent Widget with backgrounds Image Example")

    # Apply a backgrounds image using a stylesheet
    main_window.setStyleSheet("""
        QWidget {
            backgrounds-image: url('assets/bg.jpg');  /* Replace with your image path */
            backgrounds-position: center;
            backgrounds-repeat: no-repeat;
            backgrounds-size: cover;
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
