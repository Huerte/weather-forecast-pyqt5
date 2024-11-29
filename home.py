import datetime as dt
import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class HomePage:
    def __init__(self, stack_widget):
        self.stack_widget = stack_widget

    def display(self):
        home_page = QWidget()
        main_layout = QVBoxLayout()

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
                margin: 10px 10px 0, 0;
                background-color: #f02222;
            }
            QPushButton:hover {
                background-color: #f78b8b;
            }
        ''')
        logout_btn.clicked.connect(lambda: self.stack_widget.setCurrentIndex(0))
        banner.setFixedHeight(80)  # Set fixed height to occupy vertical space
        banner_layout.addWidget(logout_btn, alignment=Qt.AlignTop | Qt.AlignRight)
        banner.setLayout(banner_layout)
        main_layout.addWidget(banner)

        # Header Page (Search Bar Section)
        header_page = QWidget()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

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
        self.icon = QIcon("assets/icons/search_icon.png")
        search_btn.setIcon(self.icon)
        search_btn.setFixedSize(60, 40)
        search_btn.clicked.connect(lambda: self.get_weather())
        header_layout.addWidget(search_btn)

        header_page.setFixedHeight(60)  # Ensure header takes vertical space
        header_page.setLayout(header_layout)
        main_layout.addWidget(header_page)

        # Label Section
        label = QLabel("Home Pages")
        label.setStyleSheet("color: white;")
        label.setFixedHeight(40)  # Space occupied by label
        main_layout.addWidget(label, alignment=Qt.AlignCenter)

        home_page.setLayout(main_layout)
        return home_page

    def get_weather(self):
        if not self.search_input.text() and self.search_input.text().strip() == "":
            return

        try:
            Base_Url = "https://api.openweathermap.org/data/2.5/weather?"
            API_Key = "369f96624e904f3c1ffeaa66a10828ee"
            CITY = self.search_input.text().title()

            def kelvin_to_celsius_fahrenheit(kelvin):
                celsius = kelvin - 273.15
                fahrenheit = celsius * (9 / 5) + 32
                return celsius, fahrenheit

            url = Base_Url + "appid=" + API_Key + "&q=" + CITY

            response = requests.get(url).json()

            temp_kelvin = response['main']['temp']
            temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
            feels_like_kelvin = response['main']['feels_like']
            feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
            wind_speed = response['wind']['speed']
            humidity = response['main']['humidity']
            description = response['weather'][0]['description']

            # Define timezone offset
            timezone_offset = response['timezone']

            # Convert the timestamps to timezone-aware datetime objects
            sunrise_time = dt.datetime.fromtimestamp(response['sys']['sunrise'],
                                                     tz=dt.timezone(dt.timedelta(seconds=timezone_offset)))
            sunset_time = dt.datetime.fromtimestamp(response['sys']['sunset'],
                                                    tz=dt.timezone(dt.timedelta(seconds=timezone_offset)))

            print(f"Temperature in {CITY}: {temp_celsius:.2f}°C or {temp_fahrenheit}°F")
            print(f"Temperature in {CITY}: feels like: {feels_like_celsius:.2f}°C or {feels_like_fahrenheit}")
            print(f"Humidity in {CITY}: {humidity}%")
            print(f"Wind Speed in {CITY}: {wind_speed}m/s")
            print(f"General Weather in {CITY}: {description}")
            print(f"Sun rises in {CITY} at {sunrise_time} local time.")
            print(f"Sun sets in {CITY} at {sunset_time} local time.")
        except Exception as e:
            print(f"Error Found: {e}")
            
'''
        self.setWindowTitle("Progress Bar Example")
        self.setGeometry(200, 200, 300, 150)

        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        # Create ProgressBar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        layout.addWidget(self.progress_bar)

        # Create a button to start progress
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_progress)
        layout.addWidget(self.start_button)

        # Timer for updating progress
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)

        self.progress_value = 0

    def start_progress(self):
        self.progress_value = 0
        self.progress_bar.setValue(self.progress_value)
        self.timer.start(100)  # Update every 100 ms

    def update_progress(self):
        if self.progress_value < 100:
            self.progress_value += 1
            self.progress_bar.setValue(self.progress_value)
        else:
            self.timer.stop()

'''