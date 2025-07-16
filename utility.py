import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")


class Weather:
    def __init__(self) -> None:
        pass

    def get_weather_city_json(self, city: str, units: str = "metric"):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units={units}&appid={api_key}"
            response = requests.get(url)
            data = response.json()
            return data

        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"

    def fetch_temp(self, city: str, units: str = "metric"):
        data = self.get_weather_city_json(city, units)
        temperature = data["main"]["temp"]
        return temperature

    def fetch_humid(self, city: str, units: str = "metric"):
        data = self.get_weather_city_json(city, units)
        humidity = data["main"]["humidity"]
        return humidity

    def fetch_desc(self, city: str, units: str = "metric"):
        data = self.get_weather_city_json(city, units)
        desc = data["weather"][0]["description"]
        return desc.capitalize()
