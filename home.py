import sys

import pycountry
import requests
from io import BytesIO
from datetime import datetime
from PyQt5.QtWidgets import QWidget, QMessageBox, QVBoxLayout, \
    QHBoxLayout, QLabel, QPushButton, QLineEdit, QStackedWidget, \
    QFrame, QScrollArea, QComboBox, QGraphicsOpacityEffect, QMainWindow
from PyQt5.QtCore import Qt, QPoint, QSize, QEasingCurve, QPropertyAnimation
from PyQt5.QtGui import QIcon, QFont, QPixmap, QColor
from scipy.stats import alpha

from WeatherRequest import WeatherThread
from LocationRequest import GeocodingThread
from message_display import show_error_message
from icon_color_changer import change_icon_color


class HomePage:
    def __init__(self, main_window, stack_widget: QStackedWidget, loading_overlay):
        self.cloudiness_label = None
        self.cloudiness_icon = None
        self.cloudiness_measure = None
        self.description_def = None
        self.null_widget = None
        self.description_label = None
        self.icon_label = None
        self.time_label = None
        self.current_weather_label = None
        self.week_day_label = None
        self.location_icon = None
        self.label_list = None
        self.date_label = None
        self.weather_sect_bg = QColor(255, 255, 255, int(0.4 * 255))
        self.header_page = None
        self.search_btn = None
        self.main_window = main_window
        self.lower_section = QWidget()
        self.feels_like_label = QLabel()
        self.top_section = QWidget()
        self.feels_like_celsius = None
        self.temp_celsius = None
        self.wind_speed = None
        self.temp_label = QLabel()
        self.wind_speed_measure = QLabel()
        self.font_color = "#f0f0f5"
        self.current_metrics = "m/s"
        self.current_temp_metrics = "Celsius"
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
        top_layout.setContentsMargins(0, 0, 0, 0)

        banner = QWidget()
        banner_layout = QVBoxLayout()
        banner_layout.setContentsMargins(-5, -5, 0, 0)
        banner_layout.setSpacing(0)

        self.menu_btn = QPushButton()
        self.menu_btn.setIcon(QIcon("assets/icons/menu.png"))
        self.menu_btn.setIconSize(QSize(70, 50))
        self.menu_btn.clicked.connect(lambda: self.open_menu())
        self.menu_btn.setStyleSheet(f"color: {self.font_color}; background-color: transparent;")
        self.menu_btn.setFocusPolicy(Qt.NoFocus)
        change_icon_color(self.menu_btn, "assets/icons/menu.png", self.font_color)
        self.menu_panel = QWidget(self.home_page)
        self.menu_panel.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.menu_panel.setGeometry(0, 0, self.MENU_PANEL_WIDTH, self.MENU_PANEL_WIDTH)
        self.menu_panel.setContentsMargins(0, 0, 0, 0)

        # Semi-transparent menu panel
        self.menu_panel.setStyleSheet("background-color: rgba(0, 0, 0, 0.1); border-radius: 5px;")
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
        self.header_page = QWidget()
        self.header_page.setContentsMargins(10, 0, 10, 0)
        self.header_page.setStyleSheet(f"background-color: rgba(0, 0, 0, 0.6); border: 2px solid {self.font_color}; border-radius: 25px;")

        self.header_page.setFixedWidth(330)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(5)

        self.search_btn = QPushButton()
        self.search_btn.setIconSize(QSize(30, 30))
        self.search_btn.setFocusPolicy(Qt.NoFocus)
        self.search_btn.setStyleSheet('''
                    QPushButton {
                        font-size: 15px;
                        border: none;
                        margin: none;
                    }
                    QPushButton:hover {
                        opacity: 0.8;
                    }
                ''')
        self.search_btn.setIcon(QIcon("assets/icons/search_icon.png"))
        self.search_btn.setFixedSize(40, 30)
        self.search_btn.clicked.connect(self.get_weather)
        change_icon_color(self.search_btn, "assets/icons/search_icon.png", self.font_color)
        header_layout.addWidget(self.search_btn)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter the city")
        self.search_input.returnPressed.connect(self.get_weather)
        self.search_input.setStyleSheet(f"font-size: 15px; padding: 0px 5px; border: none; color: {self.font_color}")

        self.search_input.setFixedHeight(40)
        header_layout.addWidget(self.search_input)

        self.header_page.setFixedHeight(50)
        self.header_page.setLayout(header_layout)
        top_layout.addWidget(self.header_page, alignment=Qt.AlignRight)

        top_widget = QWidget()
        top_widget.setLayout(top_layout)
        top_widget.setStyleSheet("margin-top: 0px;")

        self.main_layout.addWidget(top_widget, alignment=Qt.AlignTop)

        if not self.get_current_location():
            self.loading_overlay.hide()
            sys.exit() #dili mo display an main window!!!

        self.home_page.setLayout(self.main_layout)

        self.loading_overlay.hide()
        return self.home_page

    def update_background(self, description):
        if "clear" in description:
            background_image = "assets/backgrounds/sunny.jpg"
        elif "clouds" in description:
            background_image = "assets/backgrounds/cloudy.jpg"
            self.search_input.setStyleSheet("color: black;")
        elif "rain" in description or "drizzle" in description:
            background_image = "assets/backgrounds/rainy.jpg"
        elif "thunderstorm" in description:
            background_image = "assets/backgrounds/thunderstorm.jpg"
            self.font_color = "#000000"
        elif "snow" in description:
            background_image = "assets/backgrounds/snowy.jpg"
        elif "mist" in description or "fog" in description or "haze" in description:
            background_image = "assets/backgrounds/foggy.jpg"
        elif "tornado" in description:
            background_image = "assets/backgrounds/tornado.jpg"
            self.font_color = "#000000"
        elif "hurricane" in description:
            background_image = "assets/backgrounds/hurricane.jpg"
        elif "windy" in description:
            background_image = "assets/backgrounds/windy.jpg"
        elif "hail" in description:
            background_image = "assets/backgrounds/hail.jpg"
        else:
            background_image = "assets/backgrounds/default.jpg"

        if self.temp_celsius < 10:
            background_image = "assets/backgrounds/cold.jpg"
        elif self.temp_celsius > 30:
            background_image = "assets/backgrounds/hot.jpg"

        self.main_window.setStyleSheet(f"""
            QMainWindow {{
                background-image: url({background_image});
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }}
        """)
        self.update_top_section()

    def update_top_section(self):
        change_icon_color(self.menu_btn, "assets/icons/menu.png", self.font_color)
        change_icon_color(self.search_btn, "assets/icons/search_icon.png", self.font_color)
        self.header_page.setStyleSheet(f"background-color: transparent; border: 2px solid {self.font_color}; border-radius: 25px;")
        self.search_input.setStyleSheet(f"font-size: 15px; padding: 0px 5px; border: none; color: {self.font_color}")

    def get_current_location(self):
        try:
            data = self.get_location()
            city = data['city']
            coordinates = data['loc'].split(',')
            self.fetch_weather_data(coordinates[0], coordinates[1])
            self.city_name = city
            self.country = data['country']
            return True
        except Exception as e:
            return False

    def get_weather(self):
        city = self.search_input.text().title()
        if not city:
            show_error_message(self.home_page, "Empty field detected", "Please provide the\nname of the city")
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
        self.main_layout.removeWidget(self.result_label)
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
        self.temp_celsius = temp_kelvin
        self.feels_like_celsius = data['main']['feels_like']
        description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        self.wind_speed = data['wind']['speed']
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

        self.update_background(description)

        self.top_section = QWidget()
        self.top_section.setObjectName('top_widget')
        self.top_section.setStyleSheet('''
            QWidget#top_widget {
                background-color: rgba(0, 0, 0, 0.2);
                border-radius: 15px;            
            }
        ''')
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)

        # Create widgets for each data point
        top_left_section = QWidget()
        top_left_layout = QVBoxLayout()
        top_left_section.setContentsMargins(10, 0, 10, 0)

        self.date_label = QLabel(f"Today, {current_day} {current_month}")
        self.date_label.setStyleSheet(f"font-size: 15px; color: {self.font_color}")
        top_left_layout.addWidget(self.date_label)

        city_label_widget = QWidget()
        city_label_layout = QHBoxLayout()
        city_label_layout.setContentsMargins(0, 0, 0, 0)

        self.location_icon = QLabel()
        self.location_icon.setStyleSheet(f"color: {self.font_color}")
        self.location_icon.setFixedSize(30, 30)
        self.location_icon.setScaledContents(True)
        self.location_icon.setContentsMargins(0, 0, 0, 0)
        pixmap = QPixmap("assets/icons/location.png")
        self.location_icon.setPixmap(pixmap)
        change_icon_color(self.location_icon, "assets/icons/location.png",  self.font_color)
        city_label_layout.addWidget(self.location_icon)

        self.city_label = QLabel(f"{self.city_name}, {self.country}")
        self.city_label.setFont(QFont("Arial", 15))
        self.city_label.setStyleSheet(f"margin: 0px; color: {self.font_color}")
        city_label_layout.addWidget(self.city_label, alignment=Qt.AlignLeft)

        city_label_widget.setLayout(city_label_layout)
        top_left_layout.addWidget(city_label_widget, alignment=Qt.AlignLeft)

        self.week_day_label = QLabel(current_weekday)
        self.week_day_label.setFont(QFont("Arial", 23, QFont.Bold))
        self.week_day_label.setStyleSheet(f"color: {self.font_color}")
        top_left_layout.addWidget(self.week_day_label, alignment=Qt.AlignLeft)

        temperature_widget = QWidget()
        temperature_layout = QHBoxLayout()
        temperature_layout.setContentsMargins(0, 0, 0, 0)

        temp_widget = QWidget()
        temp_layout = QVBoxLayout()
        temp_layout.setContentsMargins(0, 0, 0, 0)

        self.on_temp_unit_changed(self.current_temp_metrics)
        self.temp_label.setFont(QFont("Arial", 45, QFont.Bold))
        self.temp_label.setStyleSheet(f"color: {self.font_color}")
        temp_layout.addWidget(self.temp_label, alignment=Qt.AlignLeft)

        self.current_weather_label = QLabel("Current Weather")
        self.current_weather_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.current_weather_label.setStyleSheet(f"color: {self.font_color}")
        temp_layout.addWidget(self.current_weather_label, alignment=Qt.AlignLeft)

        self.time_label = QLabel(current_time)
        self.time_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.time_label.setStyleSheet(f"color: {self.font_color}")
        temp_layout.addWidget(self.time_label, alignment=Qt.AlignLeft)

        temp_widget.setLayout(temp_layout)
        temperature_layout.addWidget(temp_widget, alignment=Qt.AlignLeft)

        feels_like_widget = QWidget()
        feels_like_layout = QVBoxLayout()
        feels_like_widget.setContentsMargins(50, 0, 0, 0)

        self.on_temp_unit_changed(self.current_temp_metrics)
        self.feels_like_label.setFont(QFont("Arial", 40))
        feels_like_layout.addWidget(self.feels_like_label, alignment=Qt.AlignTop)

        self.feels_like_label_def = QLabel(f"Feels Like")
        self.feels_like_label_def.setFont(QFont("Arial", 12, QFont.Bold))
        self.feels_like_label.setStyleSheet(f"color: {self.font_color}")
        self.feels_like_label_def.setStyleSheet(f"color: {self.font_color}")
        feels_like_layout.addWidget(self.feels_like_label_def, alignment=Qt.AlignTop)

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
            self.icon_label = QLabel()
            self.icon_label.setStyleSheet(f"color: {self.font_color}")
            self.icon_label.setPixmap(icon_pixmap)
            self.icon_label.setFixedSize(250, 250)
            self.icon_label.setScaledContents(True)

            top_right_layout.addWidget(self.icon_label)
        except requests.exceptions.RequestException as e:
            print(f"Failed to load weather icon: {e}")

        top_right_section.setLayout(top_right_layout)

        top_layout.addWidget(top_left_section, alignment=Qt.AlignLeft)
        top_layout.addWidget(top_right_section, alignment=Qt.AlignLeft)
        self.top_section.setLayout(top_layout)

        self.lower_section = QWidget()
        self.lower_section.setObjectName('low_widget')
        self.lower_section.setStyleSheet('''
            QWidget#low_widget {
            background-color: rgba(0, 0, 0, 0.2);
            border-radius: 15px;
            padding: 5px 20px 5px 20px;        
            }
        ''')
        self.lower_section.setMinimumHeight(150)
        lower_layout = QHBoxLayout()
        self.lower_section.setContentsMargins(0, 0, 0, 0)

        humidity_section = QWidget()
        humidity_layout = QVBoxLayout()
        humidity_layout.setContentsMargins(20, 0, 20, 0)

        self.humidity_label = QLabel("Humidity")
        self.humidity_icon = QLabel()
        self.humidity_icon.setFixedSize(50, 50)
        self.humidity_icon.setScaledContents(True)
        self.humidity_icon.setContentsMargins(0, 0, 0, 0)
        self.humidity_icon_pixmap = QPixmap("assets/icons/humidity.png")
        self.humidity_icon.setPixmap(self.humidity_icon_pixmap)
        self.humidity_icon.setStyleSheet(f"color: {self.font_color}")
        change_icon_color(self.humidity_icon, "assets/icons/humidity.png", self.font_color)
        humidity_measure = QLabel(f"{humidity}%")
        self.humidity_label.setStyleSheet(f"font-size: 15px; color: {self.font_color};")
        humidity_measure.setStyleSheet(f"font-size: 30px; color: {self.font_color}")

        humidity_layout.addWidget(self.humidity_label, alignment=Qt.AlignTop | Qt.AlignCenter)
        humidity_layout.addWidget(self.humidity_icon, alignment=Qt.AlignCenter)
        humidity_layout.addWidget(humidity_measure, alignment=Qt.AlignCenter)
        humidity_section.setLayout(humidity_layout)

        wind_speed_section = QWidget()
        wind_speed_layout = QVBoxLayout()
        wind_speed_layout.setContentsMargins(20, 0, 20, 0)

        self.wind_speed_label = QLabel("Wind Speed")
        self.wind_icon = QLabel()
        self.wind_icon.setFixedSize(50, 50)
        self.wind_icon.setScaledContents(True)
        self.wind_icon.setContentsMargins(0, 0, 0, 0)
        self.wind_icon_pixmap = QPixmap("assets/icons/air.png")
        self.wind_icon.setPixmap(self.wind_icon_pixmap)
        self.wind_icon.setStyleSheet(f"color: {self.font_color}")
        change_icon_color(self.wind_icon, "assets/icons/air.png", self.font_color)
        self.on_wind_speed_unit_changed(self.current_metrics)
        self.wind_speed_label.setStyleSheet(f"font-size: 15px; color: {self.font_color};")
        self.wind_speed_measure.setStyleSheet(f"font-size: 30px; color: {self.font_color}")

        wind_speed_layout.addWidget(self.wind_speed_label, alignment=Qt.AlignTop | Qt.AlignCenter)
        wind_speed_layout.addWidget(self.wind_icon, alignment=Qt.AlignCenter)
        wind_speed_layout.addWidget(self.wind_speed_measure, alignment=Qt.AlignCenter)
        wind_speed_section.setLayout(wind_speed_layout)
        wind_speed_section.setLayout(wind_speed_layout)

        pressure_section = QWidget()
        pressure_layout = QVBoxLayout()
        pressure_layout.setContentsMargins(20, 0, 20, 0)

        self.pressure_label = QLabel("Pressure")
        self.pressure_icon = QLabel()
        self.pressure_icon.setFixedSize(50, 50)
        self.pressure_icon.setScaledContents(True)
        self.pressure_icon.setContentsMargins(0, 0, 0, 0)
        pressure_icon_pixmap = QPixmap("assets/icons/air pressure.png")
        self.pressure_icon.setPixmap(pressure_icon_pixmap)
        self.pressure_icon.setStyleSheet(f"color: {self.font_color}")
        change_icon_color(self.pressure_icon, "assets/icons/air pressure.png", self.font_color)
        pressure_measure = QLabel(f"{pressure} hPa")
        self.pressure_label.setStyleSheet(f"font-size: 15px; color: {self.font_color};")
        pressure_measure.setStyleSheet(f"font-size: 30px; color: {self.font_color}")

        pressure_layout.addWidget(self.pressure_label, alignment=Qt.AlignTop | Qt.AlignCenter)
        pressure_layout.addWidget(self.pressure_icon, alignment=Qt.AlignCenter)
        pressure_layout.addWidget(pressure_measure, alignment=Qt.AlignCenter)
        pressure_section.setLayout(pressure_layout)

        cloudiness_section = QWidget()
        cloudiness_layout = QVBoxLayout()
        cloudiness_layout.setContentsMargins(20, 0, 20, 0)

        self.cloudiness_label = QLabel("Cloudiness")
        self.cloudiness_icon = QLabel()
        self.cloudiness_icon.setFixedSize(50, 50)
        self.cloudiness_icon.setScaledContents(True)
        self.cloudiness_icon.setContentsMargins(0, 0, 0, 0)
        cloudiness_icon_pixmap = QPixmap("assets/icons/cloud.png")
        self.cloudiness_icon.setPixmap(cloudiness_icon_pixmap)
        self.cloudiness_icon.setStyleSheet(f"color: {self.font_color}")
        change_icon_color(self.cloudiness_icon, "assets/icons/cloud.png", self.font_color)
        self.cloudiness_measure = QLabel(f"{cloudiness}%")
        self.cloudiness_label.setStyleSheet(f"font-size: 15px; color: {self.font_color};")
        self.cloudiness_measure.setStyleSheet(f"font-size: 30px; color: {self.font_color}")

        cloudiness_layout.addWidget(self.cloudiness_label, alignment=Qt.AlignTop | Qt.AlignCenter)
        cloudiness_layout.addWidget(self.cloudiness_icon, alignment=Qt.AlignCenter)
        cloudiness_layout.addWidget(self.cloudiness_measure, alignment=Qt.AlignCenter)
        cloudiness_section.setLayout(cloudiness_layout)

        description_section = QWidget()
        description_layout = QVBoxLayout()
        description_layout.setContentsMargins(20, 0, 20, 0)

        self.description_def = QLabel("Description")
        self.null_widget = QLabel()
        self.description_label = QLabel(f"{description.capitalize()}")
        self.description_def.setStyleSheet(f"font-size: 15px; color: {self.font_color};")
        self.description_label.setStyleSheet(f"font-size: 30px; color: {self.font_color}")
        description_layout.addWidget(self.description_def, alignment=Qt.AlignTop | Qt.AlignCenter)
        description_layout.addWidget(self.description_label, alignment=Qt.AlignTop | Qt.AlignCenter)
        description_layout.addWidget(self.null_widget, alignment=Qt.AlignCenter)
        description_section.setLayout(description_layout)

        lower_layout.addWidget(humidity_section, alignment=Qt.AlignTop)
        lower_layout.addWidget(wind_speed_section, alignment=Qt.AlignTop)
        lower_layout.addWidget(pressure_section, alignment=Qt.AlignTop)
        lower_layout.addWidget(cloudiness_section, alignment=Qt.AlignTop)
        lower_layout.addWidget(description_section, alignment=Qt.AlignTop)
        self.lower_section.setLayout(lower_layout)

        self.top_section = self.top_section
        self.lower_section = self.lower_section
        self.adjust_section_widths()

        weather_layout.addWidget(self.top_section, alignment=Qt.AlignCenter)
        weather_layout.addWidget(self.lower_section, alignment=Qt.AlignCenter)

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

    def adjust_section_widths(self):
        # Get the current widths of the top and lower sections
        top_width = self.top_section.sizeHint().width()
        lower_width = self.lower_section.sizeHint().width()

        # Determine the maximum width needed
        max_width = max(top_width, lower_width)

        # Set the maximum width for both sections
        self.top_section.setMinimumWidth(max_width)
        self.lower_section.setMinimumWidth(max_width)

    @staticmethod
    def set_transparent_background(widget):
        widget.setStyleSheet("background: transparent; border: none;")

    def get_location(self):
        try:
            # Make a request to ipinfo.io API
            response = requests.get("https://ipinfo.io/json", timeout=5)
            # Check if the response is successful
            if response.status_code != 200:
                raise Exception("Failed to fetch location data")

            data = response.json()
            # Extract and process the country name
            country_code = data.get("country")
            country_name = (
                pycountry.countries.get(alpha_2=country_code).name if country_code else "Unknown"
            )

            return {
                "city": data.get("city", "Unknown"),
                "loc": data.get("loc", "Unknown"),
                "country": country_name,
            }
        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            show_error_message(self.main_window, "No Internet Connection!",
                        "Please connect your device to the internet.")
        except Exception as e:
            # Handle other unexpected errors
            show_error_message(self.main_window, "Error!", f"An error occurred: {str(e)}")

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

        # Temperature unit chooser
        self.temp_unit_label = QLabel("Choose Temperature Unit:")
        temp_unit_chooser = QComboBox()
        temp_unit_chooser.addItems(["Celsius", "Fahrenheit", "Kelvin"])
        temp_unit_chooser.setCurrentIndex(0)  # Default selection
        self.temp_unit_label.setStyleSheet("color: white;")
        temp_unit_chooser.setStyleSheet("font-size: 15px; background-color: white;")
        temp_unit_chooser.currentTextChanged.connect(self.on_temp_unit_changed)  # Connect to slot
        settings_layout.addWidget(self.temp_unit_label)
        settings_layout.addWidget(temp_unit_chooser)

        # Wind speed unit chooser
        self.wind_speed_unit_label = QLabel("Choose Wind Speed Unit:")
        wind_speed_unit_chooser = QComboBox()
        wind_speed_unit_chooser.addItems(["m/s", "km/h", "mph"])
        wind_speed_unit_chooser.setCurrentIndex(0)  # Default selection
        self.wind_speed_unit_label.setStyleSheet("color: white")
        wind_speed_unit_chooser.setStyleSheet("font-size: 15px; background-color: white;")
        wind_speed_unit_chooser.currentTextChanged.connect(self.on_wind_speed_unit_changed)  # Connect to slot
        settings_layout.addWidget(self.wind_speed_unit_label)
        settings_layout.addWidget(wind_speed_unit_chooser)

        # Set layout
        settings_page.setLayout(settings_layout)
        return settings_page

    def on_temp_unit_changed(self, value):
        self.current_temp_metrics = value
        if value == "Celsius":
            self.temp_label.setText(f"{self.temp_celsius: .2f} °C")
            self.feels_like_label.setText(f"{self.feels_like_celsius: .2f} °C")
        elif value == "Fahrenheit":
            fahrenheit = (self.temp_celsius * 9/5) + 32
            feels_like_fahrenheit = (self.feels_like_celsius * 9/5) + 32
            self.temp_label.setText(f"{fahrenheit: .2f} °F")
            self.feels_like_label.setText(f"{feels_like_fahrenheit: .2f} °F")
        else:
            kelvin = self.temp_celsius + 273.15
            feels_like_kelvin = self.feels_like_celsius + 273.15
            self.temp_label.setText(f"{kelvin: .2f} K")
            self.feels_like_label.setText(f"{feels_like_kelvin: .2f} K")

    def on_wind_speed_unit_changed(self, value):
        self.current_metrics = value
        if value == "m/s":
            self.wind_speed_measure.setText(f"{self.wind_speed: .2f} m/s")
        elif value == "km/h":
            kilometer = self.wind_speed * 3.6
            self.wind_speed_measure.setText(f"{kilometer: .2f} km/h")
        else:
            mph = self.wind_speed/1.609
            self.wind_speed_measure.setText(f"{mph: .2f} mph")

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

        # Remove the scroll area if it exists
        if hasattr(self, 'scroll_area') and self.scroll_area:
            self.main_layout.removeWidget(self.scroll_area)

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
        show_error_message(self.home_page, "An error occurred", error_message)

