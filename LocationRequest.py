from PyQt5.QtCore import QThread, pyqtSignal
import requests

class GeocodingThread(QThread):
    data_ready = pyqtSignal(dict)  # Signal to emit the response data
    error_occurred = pyqtSignal(str)  # Signal to emit error messages

    def __init__(self, city_name):
        super().__init__()
        self.city_name = city_name  # The city name for geocoding

    def run(self):
        try:
            API_KEY = "8b10c16a96250f6c3cba0ad441fe8e91"  # Replace with your OpenCage API key
            Base_Url = "http://api.positionstack.com/v1/forward"

            # Construct the URL using the city name
            url = f"{Base_Url}?access_key={API_KEY}&query={self.city_name}"

            # Make the API request
            response = requests.get(url, timeout=10).json()
            print(response)

            if 'data' in response and response['data']:
                latitude = response['data'][0]['latitude']
                longitude = response['data'][0]['longitude']
                city = response['data'][0]['name']
                country = response['data'][0]['country']

                self.data_ready.emit({
                    "city": city,
                    "latitude": latitude,
                    "longitude": longitude,
                    "country": country,
                })
            else:
                raise Exception("City not found or invalid API response.")

        except requests.exceptions.ConnectionError:
            self.error_occurred.emit("Network error: Please check your internet connection.")
        except requests.exceptions.Timeout:
            self.error_occurred.emit("Network error: Request timed out.")
        except requests.exceptions.RequestException as e:
            self.error_occurred.emit(f"Network error: {str(e)}")
        except Exception as e:
            self.error_occurred.emit(f"An error occurred: {str(e)}")