import requests
from configure import get_api_key

api_key = get_api_key()


class Weather:
    def __init__(self) -> None:
        pass

    def get_weather_city_json(self, location: str, units: str = "metric") -> str:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&units={units}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data

        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 404:
                return f"404 Error: Place Not Found"
            else:
                return f"HTTP Error"
        except requests.exceptions.ConnectionError as errc:
            return f"Connection Error"
        except requests.exceptions.Timeout as errt:
            return f"Timeout Error"
        except requests.exceptions.RequestException as e:
            return f"An unexpected error occurred"

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