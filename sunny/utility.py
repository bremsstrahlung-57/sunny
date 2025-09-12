import requests
import sys
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
