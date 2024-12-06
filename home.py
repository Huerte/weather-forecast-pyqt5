import pycountry
import requests
from io import BytesIO
from datetime import datetime
from PyQt5.QtWidgets import QWidget, QMessageBox, QVBoxLayout, \
    QHBoxLayout, QLabel, QPushButton, QLineEdit, QStackedWidget, \
    QFrame, QScrollArea, QStyle
from PyQt5.QtCore import Qt, QPoint, QSize
from PyQt5.QtGui import QIcon, QFont, QPixmap, QMovie
from WeatherRequest import WeatherThread
from LocationRequest import GeocodingThread
from Loading import LoadingOverlay


class HomePage:
    def __init__(self, stack_widget: QStackedWidget, loading_overlay):
        self.font_color = "#edeef1"
        self.country = None
        self.thread = None
        self.loading_overlay = loading_overlay
        self.scroll_area = None
        self.city_name = None
        self.home_stack_widget = None
        self.home_page = None
        self.menu_btn = None
        self.result_label = None
        self.city_label = None
        self.search_input = None
        self.main_layout = None
        self.menu_panel = None
        self.weather_thread = None
        self.MENU_PANEL_WIDTH = 200
        self.stack_widget = stack_widget
        self.current_theme_dark = True

    def display(self):
        self.loading_overlay.show()

        self.home_page = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 10, 0, 0)

        # Banner (Log Out Section)
        banner = QWidget()
        banner.setStyleSheet("margin-top: -5px;")
        banner_layout = QVBoxLayout()
        banner_layout.setContentsMargins(-5, -5, 0, 0)
        banner_layout.setSpacing(0)

        self.menu_btn = QPushButton()
        self.menu_btn.setIcon(QIcon("assets/icons/menu1.png"))
        self.menu_btn.setIconSize(QSize(30, 30))
        self.menu_btn.clicked.connect(lambda: self.open_menu())
        self.menu_btn.setStyleSheet(f"color: {self.font_color}; background-color: transparent;")
        self.menu_btn.setFocusPolicy(Qt.NoFocus)
        self.menu_panel = QWidget(self.home_page)
        self.menu_panel.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.menu_panel.setGeometry(0, 0, self.MENU_PANEL_WIDTH, self.MENU_PANEL_WIDTH)
        self.menu_panel.setContentsMargins(0, 0, 0, 0)

        # Semi-transparent menu panel
        self.menu_panel.setStyleSheet("background-color: rgba(0, 0, 0, 0.23); border-radius: 5px;")
        self.menu_panel.hide()

        menu_layout = QVBoxLayout()

        self.home_stack_widget = QStackedWidget()

        menu_buttons_widget = self.display_widgets()
        settings_window = self.display_settings()

        self.home_stack_widget.addWidget(menu_buttons_widget)
        self.home_stack_widget.addWidget(settings_window)

        menu_layout.addWidget(self.home_stack_widget)

        self.menu_panel.setLayout(menu_layout)

        # Add the menu button to the layout
        banner_layout.addWidget(self.menu_btn)

        banner.setLayout(banner_layout)

        top_layout.addWidget(banner, alignment=Qt.AlignLeft)

        # Header Page (Search Bar Section)
        header_page = QWidget()
        header_page.setContentsMargins(10, 0, 10, 0)
        header_page.setStyleSheet('''
            QWidget {
                background-color: transparent;
                border: 2px solid white; 
                border-radius: 25px;
            }
        ''')
        header_page.setFixedWidth(330)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(5)

        search_btn = QPushButton()
        search_btn.setIconSize(QSize(30, 30))
        search_btn.setFocusPolicy(Qt.NoFocus)
        search_btn.setStyleSheet('''
                    QPushButton {
                        font-size: 15px;
                        color: white;
                        border: none;
                        margin: none;
                    }
                    QPushButton:hover {
                        opacity: 0.8;
                    }
                ''')
        search_btn.setIcon(QIcon("assets/icons/search_icon.png"))
        search_btn.setFixedSize(40, 30)
        search_btn.clicked.connect(self.get_weather)
        header_layout.addWidget(search_btn)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter the city")
        self.search_input.returnPressed.connect(self.get_weather)
        self.search_input.setStyleSheet('''
            QLineEdit {
                border: none;
                padding: 0px 5px;
                font-size: 15px;
                color: white;
            }
        ''')
        self.search_input.setFixedHeight(40)
        header_layout.addWidget(self.search_input)

        header_page.setFixedHeight(50)
        header_page.setLayout(header_layout)
        top_layout.addWidget(header_page, alignment=Qt.AlignRight)

        top_widget = QWidget()
        top_widget.setStyleSheet("margin-top: 0px;")
        top_widget.setLayout(top_layout)

        self.main_layout.addWidget(top_widget, alignment=Qt.AlignTop)

        self.city_label = QLabel()
        self.city_label.setStyleSheet("color: white")
        self.main_layout.addWidget(self.city_label)

        self.get_current_location()

        self.result_label = QLabel("Weather data will be displayed here.")
        self.result_label.setStyleSheet("color: white; font-size: 15px")
        self.main_layout.addWidget(self.result_label, alignment=Qt.AlignCenter | Qt.AlignTop)

        self.home_page.setLayout(self.main_layout)

        self.loading_overlay.hide()

        return self.home_page

    def get_current_location(self):
        data = self.get_location()
        city = data['city']
        coordinates = data['loc'].split(',')
        self.fetch_weather_data(coordinates[0], coordinates[1])
        self.city_name = city
        self.country = data['country']

    def get_weather(self):
        city = self.search_input.text().title()
        if not city:
            self.result_label.setText("Please enter a city.")
            return

        self.fetch_geocoding_data(city)

    def fetch_geocoding_data(self, city):
        self.loading_overlay.show()
        self.thread = GeocodingThread(city)
        self.thread.data_ready.connect(self.handle_data_ready)
        self.thread.error_occurred.connect(lambda error: self.display_error(error))
        self.thread.start()

    def handle_data_ready(self, data):
        latitude = data['latitude']
        longitude = data['longitude']
        self.city_name = data['city']
        self.country = data['country']
        self.fetch_weather_data(latitude, longitude)

    def fetch_weather_data(self, latitude, longitude):
        self.loading_overlay.show()
        self.weather_thread = WeatherThread(latitude, longitude)
        self.weather_thread.data_ready.connect(self.display_weather)
        self.weather_thread.error_occurred.connect(self.display_error)
        self.weather_thread.start()

    def display_weather(self, data):
        self.loading_overlay.hide()
        self.result_label.setText("")
        if hasattr(self, 'scroll_area') and self.scroll_area:
            self.main_layout.removeWidget(self.scroll_area)
            self.scroll_area.deleteLater()
            self.scroll_area = None

        # Create QScrollArea for scrolling weather details
        self.scroll_area = QScrollArea()
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setStyleSheet("border: none")
        self.scroll_area.setWidgetResizable(True)  # Allow scrollable content to resize

        temp_kelvin = data['main']['temp']
        temp_celsius = temp_kelvin
        feels_like_celsius = data['main']['feels_like']
        description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed'] * 3.6
        pressure = data['main']['pressure']
        cloudiness = data['clouds']['all']
        icon_code = data['weather'][0].get('icon', '')
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

        now = datetime.now()

        # Extract the current date and time separately
        current_day = now.strftime("%d")
        current_month = now.strftime("%B")
        current_time = now.strftime("%I:%M %p")
        current_weekday = now.strftime("%A")

        weather_layout = QVBoxLayout()
        weather_layout.setContentsMargins(0, 0, 0, 0)

        top_section = QWidget()
        top_section.setObjectName('top_widget')
        top_section.setStyleSheet('''
            QWidget#top_widget {
                background-color: rgba(255, 255, 255, 0.4);
                border-radius: 15px;            
            }
        ''')
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)

        # Create widgets for each data point
        top_left_section = QWidget()
        top_left_layout = QVBoxLayout()
        top_left_section.setContentsMargins(10, 0, 10, 0)

        date_label = QLabel(f"Today, {current_day} {current_month}")
        date_label.setStyleSheet(f"font-size: 15px; color: {self.font_color}")
        top_left_layout.addWidget(date_label)

        city_label_widget = QWidget()
        city_label_layout = QHBoxLayout()
        city_label_layout.setContentsMargins(0, 0, 0, 0)

        location_icon = QLabel()
        location_icon.setStyleSheet(f"color: {self.font_color}")
        location_icon.setFixedSize(30, 30)
        location_icon.setScaledContents(True)
        location_icon.setContentsMargins(0, 0, 0, 0)
        pixmap = QPixmap("assets/icons/location.png")
        location_icon.setPixmap(pixmap)
        city_label_layout.addWidget(location_icon)

        city_label = QLabel(f"{self.city_name}, {self.country}")
        city_label.setFont(QFont("Arial", 15))
        city_label.setStyleSheet(f"margin: 0px; color: {self.font_color}")
        city_label_layout.addWidget(city_label, alignment=Qt.AlignLeft)

        city_label_widget.setLayout(city_label_layout)
        top_left_layout.addWidget(city_label_widget, alignment=Qt.AlignLeft)

        week_day_label = QLabel(current_weekday)
        week_day_label.setFont(QFont("Arial", 23, QFont.Bold))
        week_day_label.setStyleSheet(f"color: {self.font_color}")
        top_left_layout.addWidget(week_day_label, alignment=Qt.AlignLeft)

        temperature_widget = QWidget()
        temperature_layout = QHBoxLayout()
        temperature_layout.setContentsMargins(0, 0, 0, 0)

        temp_widget = QWidget()
        temp_layout = QVBoxLayout()
        temp_layout.setContentsMargins(0, 0, 0, 0)

        temp_label = QLabel(f"{temp_celsius:.2f} °C")
        temp_label.setFont(QFont("Arial", 45, QFont.Bold))
        temp_label.setStyleSheet(f"color: {self.font_color}")
        temp_layout.addWidget(temp_label, alignment=Qt.AlignLeft)

        current_weather_label = QLabel("Current Weather")
        current_weather_label.setFont(QFont("Arial", 10, QFont.Bold))
        current_weather_label.setStyleSheet(f"color: {self.font_color}")
        temp_layout.addWidget(current_weather_label, alignment=Qt.AlignLeft)

        time_label = QLabel(current_time)
        time_label.setFont(QFont("Arial", 10, QFont.Bold))
        time_label.setStyleSheet(f"color: {self.font_color}")
        temp_layout.addWidget(time_label, alignment=Qt.AlignLeft)

        temp_widget.setLayout(temp_layout)
        temperature_layout.addWidget(temp_widget, alignment=Qt.AlignLeft)

        feels_like_widget = QWidget()
        feels_like_layout = QVBoxLayout()
        feels_like_widget.setContentsMargins(50, 0, 0, 0)

        feels_like_label = QLabel(f"{feels_like_celsius:.2f} °C")
        feels_like_label.setFont(QFont("Arial", 40))
        feels_like_layout.addWidget(feels_like_label, alignment=Qt.AlignTop)

        feels_like_label_def = QLabel(f"Feels Like")
        feels_like_label_def.setFont(QFont("Arial", 12, QFont.Bold))
        feels_like_label.setStyleSheet(f"color: {self.font_color}")
        feels_like_label_def.setStyleSheet(f"color: {self.font_color}")
        feels_like_layout.addWidget(feels_like_label_def, alignment=Qt.AlignTop)

        feels_like_widget.setLayout(feels_like_layout)
        temperature_layout.addWidget(feels_like_widget, alignment=Qt.AlignTop)

        temperature_widget.setLayout(temperature_layout)

        top_left_layout.addWidget(temperature_widget, alignment=Qt.AlignLeft)

        top_left_section.setLayout(top_left_layout)

        top_right_section = QWidget()
        top_right_layout = QVBoxLayout()

        try:
            icon_response = requests.get(icon_url)
            icon_response.raise_for_status()  # Ensure successful response
            icon_data = BytesIO(icon_response.content)  # Load icon data into BytesIO
            icon_pixmap = QPixmap()
            icon_pixmap.loadFromData(icon_data.read())  # Load QPixmap from icon data

            # Create a QLabel for the icon
            icon_label = QLabel()
            icon_label.setStyleSheet(f"color: {self.font_color}")
            icon_label.setPixmap(icon_pixmap)
            icon_label.setFixedSize(250, 250)
            icon_label.setScaledContents(True)

            top_right_layout.addWidget(icon_label)
        except requests.exceptions.RequestException as e:
            print(f"Failed to load weather icon: {e}")

        top_right_section.setLayout(top_right_layout)

        top_layout.addWidget(top_left_section)
        top_layout.addWidget(top_right_section)
        top_section.setLayout(top_layout)

        lower_section = QWidget()
        lower_section.setObjectName('low_widget')
        lower_section.setStyleSheet('''
            QWidget#low_widget {
            background-color: rgba(255, 255, 255, 0.4);
            border-radius: 15px;            }
        ''')
        lower_layout = QHBoxLayout()
        lower_section.setContentsMargins(0, 20, 0, 0)

        humidity_section = QWidget()
        humidity_layout = QVBoxLayout()
        humidity_layout.setContentsMargins(30, 0, 30, 0)

        humidity_label = QLabel("Humidity")
        humidity_icon = QLabel()
        humidity_icon.setFixedSize(50, 50)
        humidity_icon.setScaledContents(True)
        humidity_icon.setContentsMargins(0, 0, 0, 0)
        humidity_icon_pixmap = QPixmap("assets/icons/humidity.png")
        humidity_icon.setPixmap(humidity_icon_pixmap)
        humidity_icon.setStyleSheet(f"color: {self.font_color}")
        humidity_measure = QLabel(f"{humidity}%")
        humidity_label.setStyleSheet(f"font-size: 15px; color: {self.font_color};")
        humidity_measure.setStyleSheet(f"font-size: 30px; color: {self.font_color}")

        humidity_layout.addWidget(humidity_label, alignment=Qt.AlignTop | Qt.AlignCenter)
        humidity_layout.addWidget(humidity_icon, alignment=Qt.AlignCenter)
        humidity_layout.addWidget(humidity_measure, alignment=Qt.AlignCenter)
        humidity_section.setLayout(humidity_layout)

        wind_speed_section = QWidget()
        wind_speed_layout = QVBoxLayout()
        wind_speed_layout.setContentsMargins(30, 0, 30, 0)

        wind_speed_label = QLabel("Wind Speed")
        wind_icon = QLabel()
        wind_icon.setFixedSize(50, 50)
        wind_icon.setScaledContents(True)
        wind_icon.setContentsMargins(0, 0, 0, 0)
        wind_icon_pixmap = QPixmap("assets/icons/air.png")
        wind_icon.setPixmap(wind_icon_pixmap)
        wind_icon.setStyleSheet(f"color: {self.font_color}")
        wind_speed_measure = QLabel(f"{wind_speed: .2f} km/h")
        wind_speed_label.setStyleSheet(f"font-size: 15px; color: {self.font_color};")
        wind_speed_measure.setStyleSheet(f"font-size: 30px; color: {self.font_color}")

        wind_speed_layout.addWidget(wind_speed_label, alignment=Qt.AlignTop | Qt.AlignCenter)
        wind_speed_layout.addWidget(wind_icon, alignment=Qt.AlignCenter)
        wind_speed_layout.addWidget(wind_speed_measure, alignment=Qt.AlignCenter)
        wind_speed_section.setLayout(wind_speed_layout)
        wind_speed_section.setLayout(wind_speed_layout)

        pressure_section = QWidget()
        pressure_layout = QVBoxLayout()
        pressure_layout.setContentsMargins(30, 0, 30, 0)

        pressure_label = QLabel("Pressure")
        pressure_icon = QLabel()
        pressure_icon.setFixedSize(50, 50)
        pressure_icon.setScaledContents(True)
        pressure_icon.setContentsMargins(0, 0, 0, 0)
        pressure_icon_pixmap = QPixmap("assets/icons/air pressure.png")
        pressure_icon.setPixmap(pressure_icon_pixmap)
        pressure_icon.setStyleSheet(f"color: {self.font_color}")
        pressure_measure = QLabel(f"{pressure} hPa")
        pressure_label.setStyleSheet(f"font-size: 15px; color: {self.font_color};")
        pressure_measure.setStyleSheet(f"font-size: 30px; color: {self.font_color}")

        pressure_layout.addWidget(pressure_label, alignment=Qt.AlignTop | Qt.AlignCenter)
        pressure_layout.addWidget(pressure_icon, alignment=Qt.AlignCenter)
        pressure_layout.addWidget(pressure_measure, alignment=Qt.AlignCenter)
        pressure_section.setLayout(pressure_layout)

        cloudiness_section = QWidget()
        cloudiness_layout = QVBoxLayout()
        cloudiness_layout.setContentsMargins(30, 0, 30, 0)

        cloudiness_label = QLabel("Cloudiness")
        cloudiness_icon = QLabel()
        cloudiness_icon.setFixedSize(50, 50)
        cloudiness_icon.setScaledContents(True)
        cloudiness_icon.setContentsMargins(0, 0, 0, 0)
        cloudiness_icon_pixmap = QPixmap("assets/icons/cloud.png")
        cloudiness_icon.setPixmap(cloudiness_icon_pixmap)
        cloudiness_icon.setStyleSheet(f"color: {self.font_color}")
        cloudiness_measure = QLabel(f"{cloudiness}%")
        cloudiness_label.setStyleSheet(f"font-size: 15px; color: {self.font_color};")
        cloudiness_measure.setStyleSheet(f"font-size: 30px; color: {self.font_color}")

        cloudiness_layout.addWidget(cloudiness_label, alignment=Qt.AlignTop | Qt.AlignCenter)
        cloudiness_layout.addWidget(cloudiness_icon, alignment=Qt.AlignCenter)
        cloudiness_layout.addWidget(cloudiness_measure, alignment=Qt.AlignCenter)
        cloudiness_section.setLayout(cloudiness_layout)

        description_section = QWidget()
        description_layout = QVBoxLayout()
        description_layout.setContentsMargins(30, 0, 30, 0)

        description_def = QLabel("Description")
        null_widget = QLabel()
        description_label = QLabel(f"{description.capitalize()}")
        description_def.setStyleSheet(f"font-size: 15px; color: {self.font_color};")
        description_label.setStyleSheet(f"font-size: 30px; color: {self.font_color}")
        description_layout.addWidget(description_def, alignment=Qt.AlignTop | Qt.AlignCenter)
        description_layout.addWidget(description_label, alignment=Qt.AlignTop | Qt.AlignCenter)
        description_layout.addWidget(null_widget, alignment=Qt.AlignCenter)
        description_section.setLayout(description_layout)

        lower_layout.addWidget(humidity_section, alignment=Qt.AlignTop)
        lower_layout.addWidget(wind_speed_section, alignment=Qt.AlignTop)
        lower_layout.addWidget(pressure_section, alignment=Qt.AlignTop)
        lower_layout.addWidget(cloudiness_section, alignment=Qt.AlignTop)
        lower_layout.addWidget(description_section, alignment=Qt.AlignTop)
        lower_section.setLayout(lower_layout)

        weather_layout.addWidget(top_section, alignment=Qt.AlignCenter)
        weather_layout.addWidget(lower_section, alignment=Qt.AlignCenter | Qt.AlignTop)

        scroll_widget = QWidget()
        scroll_widget. setStyleSheet('''
            QWidget {
                background: transparent;
                border: none;
            }
        ''')

        scroll_widget.setContentsMargins(0, 0, 0, 0)
        scroll_widget.setLayout(weather_layout)

        # Add container widget to the scroll area
        self.scroll_area.setWidget(scroll_widget)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollArea > QWidget {
                background: transparent;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background: transparent;
            }
        """)

        # Add scroll area to the main layout
        self.main_layout.addWidget(self.scroll_area)
        self.loading_overlay.hide()

    @staticmethod
    def set_transparent_background(widget):
        """ Recursively sets the background of all child widgets to transparent. """
        widget.setStyleSheet("background: transparent; border: none;")

    @staticmethod
    def get_location():
        response = requests.get("https://ipinfo.io/json")
        data = response.json()

        country_code = data["country"]
        country_name = pycountry.countries.get(alpha_2=country_code).name if country_code else None

        return {
            "city": data["city"],
            "loc": data["loc"],
            "country": country_name

        }

    def display_settings(self):
        settings_page = QWidget()
        settings_layout = QVBoxLayout()

        # Exit button to go back to the home page
        exit_settings_btn = QPushButton()
        exit_settings_btn.setIcon(QIcon("assets/icons/back.png"))
        exit_settings_btn.setIconSize(QSize(20, 20))
        exit_settings_btn.setFocusPolicy(Qt.NoFocus)
        exit_settings_btn.setStyleSheet("background-color: #fb1d11;")
        exit_settings_btn.setFixedSize(40, 30)
        exit_settings_btn.clicked.connect(lambda: self.home_stack_widget.setCurrentIndex(0))
        settings_layout.addWidget(exit_settings_btn, alignment=Qt.AlignLeft)

        # Button to change the theme to Light Mode
        light_mode_btn = QPushButton("Switch Theme")
        light_mode_btn.setStyleSheet('''
            QPushButton {
                font-size: 16px;
                padding: 10px;
                background-color: #4CAF50; /* Green */
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049; /* Darker green on hover */
            }
        ''')
        light_mode_btn.clicked.connect(self.switch_theme)  # Connect to light mode change function
        settings_layout.addWidget(light_mode_btn, alignment=Qt.AlignCenter)

        settings_page.setLayout(settings_layout)
        return settings_page

    def switch_theme(self):
        if self.current_theme_dark:
            self.switch_to_light_mode()
        else:
            self.switch_to_dark_mode()
        self.current_theme_dark = not self.current_theme_dark

    def switch_to_dark_mode(self):
        dark_mode_stylesheet = """
                    QWidget {
                        background-color: #131621; 
                        color: white
                    }
                    QLineEdit {
                        border: 1px solid gray;
                        background-color: #131621;
                        border: none;
                    }
                    QPushButton {
                        background-color: #131621; 
                        color: white
                        border-radius: 20px;
                    }
                    QPushButton:hover {
                        background-color: #0056b3;
                    }
                    QLabel {
                        color: white
                    }
                """
        self.search_input.setStyleSheet('''QLineEdit {
            color: white;
            border: none;
            font-size: 15px;
        }''')
        self.result_label.setStyleSheet("color: white; font-size: 15px;")
        self.home_page.setStyleSheet(dark_mode_stylesheet)

    def switch_to_light_mode(self):
        light_mode_stylesheet = """
            QWidget {
                background-color: #b5c5c8;
                color: black;
            }
            QLineEdit {
                border: 1px solid gray;
                background-color: #f4f4f4;
                padding: 5px;
                border-radius: 20px;
            }
            QPushButton {
                background-color: #007BFF;
                color: #b5c5c8;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLabel {
                color: black;
            }
        """
        self.search_input.setStyleSheet('''QLineEdit {
            color: black;
            font-size: 15px;
            border: none;
        }''')
        self.result_label.setStyleSheet("color: black; font-size: 15px;")
        self.home_page.setStyleSheet(light_mode_stylesheet)

    def display_widgets(self):
        menu_layout = QVBoxLayout()
        # Settings button
        settings_btn = QPushButton("Settings")
        settings_btn.setIcon(QIcon("assets/icons/settings.png"))
        settings_btn.setIconSize(QSize(20, 20))
        settings_btn.setFocusPolicy(Qt.NoFocus)
        settings_btn.setFixedWidth(self.MENU_PANEL_WIDTH)
        settings_btn.clicked.connect(lambda: self.home_stack_widget.setCurrentIndex(1))
        settings_btn.setStyleSheet('''
                    QPushButton {
                        border: none;
                        color: white;
                        border-radius: 15px;
                        padding: 5px;
                        margin: 0px;
                        font-size: 15px;
                        background-color: inherent;
                    }
                    QPushButton:hover {
                        background-color: #5ba8f5;
                    }
                ''')
        menu_layout.addWidget(settings_btn, alignment=Qt.AlignCenter)

        menu_layout.addWidget(self.create_separator())

        logout_btn = QPushButton("Log out")
        logout_btn.setIcon(QIcon("assets/icons/exit.png"))
        logout_btn.setIconSize(QSize(20, 20))
        logout_btn.setFocusPolicy(Qt.NoFocus)
        logout_btn.setFixedWidth(self.MENU_PANEL_WIDTH)
        logout_btn.setStyleSheet('''
                    QPushButton {
                        border: none;
                        color: white;
                        border-radius: 15px;
                        padding: 5px;
                        margin: 0px;
                        font-size: 15px;
                        background-color: inherent;
                    }
                    QPushButton:hover {
                        background-color: #f78b8b;
                    }
                ''')
        logout_btn.clicked.connect(self.confirm_logout)
        menu_layout.addWidget(logout_btn, alignment=Qt.AlignCenter | Qt.AlignBottom)
        menu_layout.addStretch()
        menu = QWidget()
        menu.setLayout(menu_layout)

        return menu

    def confirm_logout(self):
        # Create a confirmation dialog
        confirmation = QMessageBox(self.home_page)
        confirmation.setStyleSheet("")
        confirmation.setIcon(QMessageBox.Warning)
        confirmation.setWindowTitle("Confirm Logout")
        confirmation.setText("Are you sure you want to log out?")
        confirmation.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        # Check the user's response
        response = confirmation.exec_()
        if response == QMessageBox.Yes:
            self.reset_home_widgets()
            self.get_current_location()
            self.stack_widget.setCurrentIndex(0)

    def reset_home_widgets(self):
        # Reset the search input
        self.search_input.clear()

        # Reset the result label
        self.result_label.setText("Weather data will be displayed here.")

        # Reset the city label
        self.city_label.setText("")

        # Remove the scroll area if it exists
        if hasattr(self, 'scroll_area') and self.scroll_area:
            self.main_layout.removeWidget(self.scroll_area)
            self.scroll_area.deleteLater()
            self.scroll_area = None

    def open_menu(self):
        if self.menu_panel.isHidden():
            pos = self.menu_btn.mapToGlobal(QPoint(-9, -9))
            self.menu_panel.move(pos)
            self.menu_panel.show()
        else:
            self.menu_panel.hide()

    @staticmethod
    def create_separator():
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setFixedHeight(1)
        line.setStyleSheet("""
            background-color: gray;
            margin: 0px;
        """)
        return line

    def display_error(self, error_message):
        self.loading_overlay.hide()
        self.result_label.setText(f"Error: {error_message}")