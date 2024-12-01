import requests
from PyQt5.QtWidgets import QWidget, QMessageBox, QVBoxLayout, \
    QHBoxLayout, QLabel, QPushButton, QLineEdit, QStackedWidget, \
    QFrame, QScrollArea
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPoint, QSize
from PyQt5.QtGui import QIcon, QFont, QPixmap
import time
from requests.exceptions import ConnectionError, Timeout, RequestException


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

            response = requests.get(url, timeout=10).json()  # Set a timeout for safety
            print(response)

            if "main" not in response:
                raise Exception("City not found or invalid API response.")

            self.data_ready.emit(response)

        except ConnectionError:
            self.error_occurred.emit("Network error: Please check your internet connection.")
        except Timeout:
            self.error_occurred.emit("Network error: Request timed out.")
        except RequestException as e:
            self.error_occurred.emit(f"Network error: {str(e)}")
        except Exception as e:
            self.error_occurred.emit(f"An error occurred: {str(e)}")


class HomePage:
    def __init__(self, stack_widget: QStackedWidget):
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

    def display(self):
        self.home_page = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)

        # Banner (Log Out Section)
        banner = QWidget()
        banner.setStyleSheet("margin-top: -5px;")
        banner_layout = QVBoxLayout()
        banner_layout.setContentsMargins(-5, -5, 0, 0)
        banner_layout.setSpacing(0)

        self.menu_btn = QPushButton()
        self.menu_btn.setIcon(QIcon("assets/icons/menu.png"))
        self.menu_btn.setIconSize(QSize(30, 30))
        self.menu_btn.clicked.connect(lambda: self.open_menu())
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
        header_page.setFixedWidth(300)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(5)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter the city")
        self.search_input.returnPressed.connect(self.get_weather)
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
        header_layout.addWidget(self.search_input)

        search_btn = QPushButton()
        search_btn.setIconSize(QSize(20, 20))
        search_btn.setFocusPolicy(Qt.NoFocus)
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
        top_layout.addWidget(header_page, alignment=Qt.AlignRight)

        top_widget = QWidget()
        top_widget.setStyleSheet("margin-top: 0px;")
        top_widget.setLayout(top_layout)

        self.main_layout.addWidget(top_widget, alignment=Qt.AlignTop)

        self.city_label = QLabel()
        self.city_label.setStyleSheet("color: white")
        self.main_layout.addWidget(self.city_label)

        self.result_label = QLabel("Weather data will be displayed here.")
        self.result_label.setStyleSheet("color: white;")
        self.main_layout.addWidget(self.result_label, alignment=Qt.AlignCenter | Qt.AlignTop)

        self.home_page.setLayout(self.main_layout)
        return self.home_page

    def display_settings(self):
        settings_page = QWidget()
        settings_layout = QVBoxLayout()

        exit_settings_btn = QPushButton("Exit")
        exit_settings_btn.setStyleSheet("background-color: red;")
        exit_settings_btn.setFixedSize(40, 30)
        exit_settings_btn.clicked.connect(lambda: self.home_stack_widget.setCurrentIndex(0))
        settings_layout.addWidget(exit_settings_btn, alignment=Qt.AlignLeft)

        settings_layout.addWidget(QLabel("Settings"), alignment=Qt.AlignCenter)

        settings_page.setLayout(settings_layout)
        return settings_page

    def display_widgets(self):
        menu_layout = QVBoxLayout()
        username = "Richard"
        username_label = QLabel(username)
        username_label.setStyleSheet("font-size: 15px; color: white; margin: 0px;")
        menu_layout.addWidget(username_label, alignment=Qt.AlignCenter)
        # Settings button
        settings_btn = QPushButton("Settings")
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
            self.stack_widget.setCurrentIndex(0)

    def open_menu(self):
        if self.menu_panel.isHidden():
            pos = self.menu_btn.mapToGlobal(QPoint(-9, -9))
            self.menu_panel.move(pos)
            self.menu_panel.show()
        else:
            self.menu_panel.hide()

    def get_weather(self):
        city = self.search_input.text().title()
        if not city:
            self.result_label.setText("Please enter a city.")
            return

        self.weather_thread = WeatherThread(city)
        self.weather_thread.data_ready.connect(self.display_weather)
        self.weather_thread.error_occurred.connect(self.display_error)
        self.weather_thread.start()

    def display_weather(self, data):
        self.result_label.setText("")
        if hasattr(self, 'scroll_area') and self.scroll_area:
            self.main_layout.removeWidget(self.scroll_area)
            self.scroll_area.deleteLater()
            self.scroll_area = None

        # Create QScrollArea for scrolling weather details
        self.scroll_area = QScrollArea()
        self.scroll_area.setStyleSheet("border: none")
        self.scroll_area.setWidgetResizable(True)  # Allow scrollable content to resize

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

        weather_layout = QVBoxLayout()###############

        # Create widgets for each data point
        left_section = QWidget()
        left_layout = QVBoxLayout()
        left_section.setContentsMargins(10, 0, 10, 0)

        city_label = QLabel(self.search_input.text().title())
        city_label.setFont(QFont("Arial", 40, QFont.Bold))
        left_layout.addWidget(city_label, alignment=Qt.AlignCenter | Qt.AlignBottom)

        left_lower_section = QWidget()
        left_lower_layout = QHBoxLayout()

        pixmap = QPixmap("assets/icons/rain_cloud.png").scaled(400, 300, aspectRatioMode=Qt.KeepAspectRatio)
        # Create a QLabel to hold the image
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        pixmap = pixmap
        # Add the QLabel to the layout
        left_lower_layout.addWidget(image_label)

        temp_label = QLabel(f"Temperature: {temp_celsius:.2f}°C")
        feels_like_label = QLabel(f"Feels Like: {feels_like_celsius:.2f}°C")

        left_lower_section.setLayout(left_lower_layout)

############################################################################


        description_label = QLabel(f"Description: {description.capitalize()}")
        humidity_label = QLabel(f"Humidity: {humidity}%")
        wind_speed_label = QLabel(f"Wind Speed: {wind_speed} m/s")
        pressure_label = QLabel(f"Pressure: {pressure} hPa")
        cloudiness_label = QLabel(f"Cloudiness: {cloudiness}%")
        visibility_label = QLabel(f"Visibility: {visibility_km:.2f} km")
        sunrise_label = QLabel(f"Sunrise: {sunrise_time}")
        sunset_label = QLabel(f"Sunset: {sunset_time}")

        # Organize widgets into layouts
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

        # Create a container widget for scroll content
        scroll_widget = QWidget()
        scroll_widget.setLayout(weather_layout)

        # Add container widget to the scroll area
        self.scroll_area.setWidget(scroll_widget)

        # Add scroll area to the main layout
        self.main_layout.addWidget(self.scroll_area)

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
        self.result_label.setText(f"Error: {error_message}")
