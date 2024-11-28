import datetime as dt
import requests

Base_Url = "https://api.openweathermap.org/data/2.5/weather?"
API_Key = "369f96624e904f3c1ffeaa66a10828ee"
CITY = "Cantilan"

def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
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
sunrise_time = dt.datetime.fromtimestamp(response['sys']['sunrise'], tz=dt.timezone(dt.timedelta(seconds=timezone_offset)))
sunset_time = dt.datetime.fromtimestamp(response['sys']['sunset'], tz=dt.timezone(dt.timedelta(seconds=timezone_offset)))

print(f"Temperature in {CITY}: {temp_celsius:.2f}°C or {temp_fahrenheit}°F")
print(f"Temperature in {CITY}: feels like: {feels_like_celsius:.2f}°C or {feels_like_fahrenheit}")
print(f"Humidity in {CITY}: {humidity}%")
print(f"Wind Speed in {CITY}: {wind_speed}m/s")
print(f"General Weather in {CITY}: {description}")
print(f"Sun rises in {CITY} at {sunrise_time} local time.")
print(f"Sun sets in {CITY} at {sunset_time} local time.")
