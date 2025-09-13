import requests
import sys
import json
from sunny.configure import ConfigManager

API_CONFIG = ConfigManager()

api_key = API_CONFIG.get_api_key
class Weather:
    def __init__(self) -> None:
        pass

    def get_weather_city_json(self, location: str, units: str = "metric") -> str:
        """Returns open weather api data of specified location and units"""
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&units={units}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.HTTPError as http_err:
            if http_err.response.status_code == 401:
                sys.exit(
                    "Error: Unauthorized. Check your API key."
                )
            elif http_err.response.status_code == 404:
                sys.exit(
                    f"Error: Location '{location}' not found."
                )
            else:
                sys.exit(f"Error: HTTP error {http_err.response.status_code}")
        except requests.exceptions.RequestException as req_err:
            sys.exit(f"Error: An error occurred with the request: {req_err}")

    def fetch_temp(self, location: str, units: str = "metric") -> float:
        data = self.get_weather_city_json(location, units)
        temperature = data["main"]["temp"]
        return temperature

    def fetch_humid(self, location: str, units: str = "metric") -> int:
        data = self.get_weather_city_json(location, units)
        humidity = data["main"]["humidity"]
        return humidity

    def fetch_desc(self, location: str, units: str = "metric") -> str:
        data = self.get_weather_city_json(location, units)
        desc = data["weather"][0]["description"]
        return desc.capitalize()

    def get_weather_forecast(self, location: str, units: str = "metric"):
        """Returns forecast data of specified location and units"""
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&units={units}&appid={api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.HTTPError as http_err:
            if http_err.response.status_code == 401:
                sys.exit("Error: Unauthorized. Check your API key.")
            elif http_err.response.status_code == 404:
                sys.exit(f"Error: Location '{location}' not found.")
            else:
                sys.exit(f"Error: HTTP error {http_err.response.status_code}")
        except requests.exceptions.RequestException as req_err:
            sys.exit(f"Error: An error occurred with the request: {req_err}")

    def fetch_forecast(self, location: str, units: str = "metric") -> list:
        """Fetches 5-day forecast data."""
        data = self.get_weather_forecast(location, units)
        forecast_data = []
        for forecast in data.get("list", []):
            forecast_data.append(
                {
                    "dt_txt": forecast.get("dt_txt"),
                    "temp": forecast.get("main", {}).get("temp"),
                    "feels_like_temp": forecast.get("main", {}).get("feels_like"),
                    "humidity": forecast.get("main", {}).get("humidity"),
                    "main": forecast.get("weather", [{}])[0].get("main"),
                    "description": forecast.get("weather", [{}])[0].get("description"),
                    "id": forecast.get("weather", [{}])[0].get("id"),
                    "icon": forecast.get("weather", [{}])[0].get("icon"),
                    "wind_speed": forecast.get("wind", {}).get("speed"),
                }
            )
        return forecast_data[0::5]
