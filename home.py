import requests
from PyQt5.QtWidgets import QWidget, QMessageBox, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QStackedWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
import time

class WeatherThread(QThread):
    data_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, city):
        super().__init__()
        self.city = city

    def run(self):
        try:
            Base_Url = "https://api.openweathermap.org/data/2.5/weather?"
            API_Key = "369f96624e904f3c1ffeaa66a10828ee"
            url = f"{Base_Url}appid={API_Key}&q={self.city}"

            response = requests.get(url).json()
            print(response)
            if "main" not in response:
                raise Exception("City not found or invalid API response.")

            self.data_ready.emit(response)
        except Exception as e:
            self.error_occurred.emit(str(e))


class HomePage:
    def __init__(self, stack_widget: QStackedWidget):
        self.stack_widget = stack_widget
        self.weather_thread = None

    def display(self):
        home_page = QWidget()
        self.main_layout = QVBoxLayout()

        # Banner (Log Out Section)

        banner = QWidget()
        banner_layout = QVBoxLayout()
        banner_layout.setContentsMargins(0, 0, 0, 0)
        banner_layout.setSpacing(0)

        logout_btn = QPushButton("Log out")
        logout_btn.setStyleSheet('''
            QPushButton {
                border: none;
                color: white;
                border-radius: 13px;      
                padding: 5px;         
                font-size: 15px;   
                margin: 10px;
                background-color: #f02222;
            }
            QPushButton:hover {
                background-color: #f78b8b;
            }
        ''')

        # Define the logout action
        def confirm_logout():
            # Create a confirmation dialog
            confirmation = QMessageBox()
            confirmation.setIcon(QMessageBox.Warning)
            confirmation.setWindowTitle("Confirm Logout")
            confirmation.setText("Are you sure you want to log out?")
            confirmation.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

            # Check the user's response
            response = confirmation.exec_()
            if response == QMessageBox.Yes:
                self.stack_widget.setCurrentIndex(0)

        # Connect the button to the confirmation function
        logout_btn.clicked.connect(confirm_logout)
        banner.setFixedHeight(80)
        banner_layout.addWidget(logout_btn, alignment=Qt.AlignTop | Qt.AlignRight)
        banner.setLayout(banner_layout)
        self.main_layout.addWidget(banner)

        # Header Page (Search Bar Section)
        header_page = QWidget()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter the city")
        self.search_input.setStyleSheet('''
            QLineEdit {
                border: 0.5px solid white;
                color: white;
                border-radius: 20px;      
                padding: 5px;         
                font-size: 15px;   
            }
        ''')
        self.search_input.setFixedHeight(40)
        self.search_input.setFixedWidth(300)
        header_layout.addWidget(self.search_input)

        search_btn = QPushButton()
        search_btn.setStyleSheet('''
            QPushButton {
                font-size: 15px;
                border-radius: 20px; 
                background-color: #007BFF;
                color: white;
            }
            QPushButton:hover {
                background-color: #0080c0;
            }
        ''')
        search_btn.setIcon(QIcon("assets/icons/search_icon.png"))
        search_btn.setFixedSize(60, 40)
        search_btn.clicked.connect(self.get_weather)
        header_layout.addWidget(search_btn)

        header_page.setFixedHeight(60)
        header_page.setLayout(header_layout)
        self.main_layout.addWidget(header_page)

        self.city_label = QLabel()
        self.city_label.setStyleSheet("color: white")
        self.main_layout.addWidget(self.city_label)

        # Weather Result Section
        self.result_label = QLabel("Weather data will be displayed here.")
        self.result_label.setStyleSheet("color: white;")
        self.main_layout.addWidget(self.result_label, alignment=Qt.AlignCenter | Qt.AlignTop)

        home_page.setLayout(self.main_layout)
        return home_page

    def get_weather(self):
        print("HEllo richard")
        city = self.search_input.text().title()
        if not city:
            self.result_label.setText("Please enter a city.")
            return

        self.weather_thread = WeatherThread(city)
        self.weather_thread.data_ready.connect(self.display_weather)
        self.weather_thread.error_occurred.connect(self.display_error)
        self.weather_thread.start()

    def display_weather(self, data):
        self.result_label.deleteLater()

        temp_kelvin = data['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        feels_like_celsius = data['main']['feels_like'] - 273.15
        description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        pressure = data['main']['pressure']
        cloudiness = data['clouds']['all']
        visibility_km = data['visibility'] / 1000
        sunrise_time = time.strftime('%H:%M:%S', time.gmtime(data['sys']['sunrise'] + data['timezone']))
        sunset_time = time.strftime('%H:%M:%S', time.gmtime(data['sys']['sunset'] + data['timezone']))

        # Create widgets for each data point
        city_label = QLabel(self.search_input.text().title())
        city_label.setFont(QFont("Arial", 24, QFont.Bold))
        city_label.setAlignment(Qt.AlignCenter)

        temp_label = QLabel(f"Temperature: {temp_celsius:.2f}°C")
        feels_like_label = QLabel(f"Feels Like: {feels_like_celsius:.2f}°C")
        description_label = QLabel(f"Description: {description.capitalize()}")
        humidity_label = QLabel(f"Humidity: {humidity}%")
        wind_speed_label = QLabel(f"Wind Speed: {wind_speed} m/s")
        pressure_label = QLabel(f"Pressure: {pressure} hPa")
        cloudiness_label = QLabel(f"Cloudiness: {cloudiness}%")
        visibility_label = QLabel(f"Visibility: {visibility_km:.2f} km")
        sunrise_label = QLabel(f"Sunrise: {sunrise_time}")
        sunset_label = QLabel(f"Sunset: {sunset_time}")

        # Style labels
        for label in [temp_label, feels_like_label, description_label, humidity_label,
                      wind_speed_label, pressure_label, cloudiness_label, visibility_label,
                      sunrise_label, sunset_label]:
            label.setFont(QFont("Arial", 14))
            label.setAlignment(Qt.AlignLeft)

        # Organize widgets into layouts
        weather_layout = QVBoxLayout()
        weather_layout.addWidget(city_label)
        weather_layout.addWidget(temp_label)
        weather_layout.addWidget(feels_like_label)
        weather_layout.addWidget(description_label)
        weather_layout.addWidget(humidity_label)
        weather_layout.addWidget(wind_speed_label)
        weather_layout.addWidget(pressure_label)
        weather_layout.addWidget(cloudiness_label)
        weather_layout.addWidget(visibility_label)
        weather_layout.addWidget(sunrise_label)
        weather_layout.addWidget(sunset_label)

        # Create main widget
        main_widget = QWidget()
        main_widget.setLayout(weather_layout)

        self.main_layout.addWidget(main_widget)

    def display_error(self, error_message):
        self.result_label.setText(f"Error: {error_message}")
