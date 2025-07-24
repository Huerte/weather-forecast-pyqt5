from PyQt5.QtCore import QThread, pyqtSignal
import requests


class WeatherThread(QThread):
    data_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, lat, lon):
        super().__init__()
        self.lat = lat
        self.lon = lon

    def run(self):
        try:
            Base_Url = "https://api.openweathermap.org/data/2.5/weather?"
            API_Key = "369f96624e904f3c1ffeaa66a10828ee"

            # Construct the URL using latitude and longitude
            url = f"{Base_Url}lat={self.lat}&lon={self.lon}&appid={API_Key}&units=metric"

            # Make the API request
            response = requests.get(url, timeout=10).json()
            print(response)

            if "main" not in response:
                raise Exception("City not found or invalid API response.")

            self.data_ready.emit(response)

        except requests.exceptions.ConnectionError:
            self.error_occurred.emit("Network error: Please check your internet connection.")
        except requests.exceptions.Timeout:
            self.error_occurred.emit("Network error: Request timed out.")
        except requests.exceptions.RequestException as e:
            self.error_occurred.emit(f"Network error: {str(e)}")
        except Exception as e:
            self.error_occurred.emit(f"An error occurred: {str(e)}")