from datetime import datetime, timedelta, timezone
from math import isfinite

import requests

from sunny.configure import ConfigManager


class WeatherError(RuntimeError):
    """A weather request or its response could not be used."""


class Weather:
    def __init__(self, api_key=None) -> None:
        self.api_key = api_key

    def _request(self, endpoint: str, location: str, units: str) -> dict:
        if self.api_key is None:
            try:
                self.api_key = ConfigManager().get_api_key
            except (OSError, ValueError, AttributeError, SystemExit):
                raise WeatherError(
                    "Unable to load the API key. Check your sunny configuration."
                ) from None
        if not isinstance(self.api_key, str) or not self.api_key.strip():
            raise WeatherError("No API key configured. Check your sunny configuration.")

        try:
            response = requests.get(
                f"https://api.openweathermap.org/data/2.5/{endpoint}",
                params={"q": location, "units": units, "appid": self.api_key},
                timeout=(5, 15),
            )
            response.raise_for_status()
        except requests.exceptions.Timeout:
            raise WeatherError(
                "The weather request timed out. Please try again."
            ) from None
        except requests.exceptions.ConnectionError:
            raise WeatherError(
                "Unable to connect to the weather service. Check your connection."
            ) from None
        except requests.exceptions.HTTPError as error:
            status = error.response.status_code if error.response is not None else None
            messages = {
                401: "Unauthorized. Check your API key.",
                404: "Location not found. Check the city name.",
                429: "Weather service rate limit reached. Please try again later.",
            }
            # fixed: request exceptions may include the URL and API key.
            raise WeatherError(
                messages.get(status, "The weather service returned an HTTP error.")
            ) from None
        except requests.exceptions.RequestException:
            raise WeatherError(
                "Unable to request weather data. Please try again."
            ) from None

        try:
            data = response.json()
        except ValueError:
            raise WeatherError("The weather service returned malformed JSON.") from None
        if not isinstance(data, dict) or not data:
            raise WeatherError("The weather service returned invalid weather data.")
        return data

    @staticmethod
    def _validate_number(value) -> None:
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not isfinite(value)
        ):
            raise ValueError

    @classmethod
    def _validate_weather(cls, data: dict, current: bool = False) -> None:
        try:
            if not isinstance(data, dict) or not isinstance(data["weather"], list):
                raise ValueError
            weather = data["weather"][0]
            numbers = [data["main"][key] for key in ("temp", "feels_like", "humidity")]
            numbers.extend((weather["id"], data["wind"]["speed"]))
            strings = [weather[key] for key in ("main", "description", "icon")]
            if current:
                numbers.extend(data["coord"][key] for key in ("lon", "lat"))
                strings.append(data["sys"]["country"])
            else:
                numbers.extend(
                    data["main"].get(key, data["main"]["temp"])
                    for key in ("temp_min", "temp_max")
                )
            for value in numbers:
                cls._validate_number(value)
            if any(
                not isinstance(value, str) or not value.strip() for value in strings
            ):
                raise ValueError
        except (KeyError, IndexError, TypeError, ValueError, OverflowError):
            raise WeatherError(
                "The weather service returned incomplete or invalid weather data."
            ) from None

    def get_weather_city_json(self, location: str, units: str = "metric") -> dict:
        """Return validated current weather for the specified location and units."""
        data = self._request("weather", location, units)
        self._validate_weather(data, current=True)
        return data

    def fetch_temp(self, location: str, units: str = "metric") -> float:
        data = self.get_weather_city_json(location, units)
        return data["main"]["temp"]

    def fetch_humid(self, location: str, units: str = "metric") -> int:
        data = self.get_weather_city_json(location, units)
        return data["main"]["humidity"]

    def fetch_desc(self, location: str, units: str = "metric") -> str:
        data = self.get_weather_city_json(location, units)
        return data["weather"][0]["description"].capitalize()

    def get_weather_forecast(self, location: str, units: str = "metric") -> dict:
        """Return validated forecast samples for the specified location and units."""
        data = self._request("forecast", location, units)
        if not isinstance(data.get("list"), list) or not data["list"]:
            raise WeatherError(
                "The weather service returned empty or invalid forecast data."
            )
        for sample in data["list"]:
            self._validate_weather(sample)
        return data

    def fetch_forecast(self, location: str, units: str = "metric") -> list:
        """Return up to five local dates, choosing each date's sample nearest noon."""
        data = self.get_weather_forecast(location, units)
        days = {}
        try:
            offset = data["city"]["timezone"]
            self._validate_number(offset)
            local_timezone = timezone(timedelta(seconds=offset))
            for sample in data["list"]:
                timestamp = sample.get("dt")
                if timestamp is None:
                    sample_time = datetime.strptime(
                        sample["dt_txt"], "%Y-%m-%d %H:%M:%S"
                    ).replace(tzinfo=timezone.utc)
                else:
                    self._validate_number(timestamp)
                    sample_time = datetime.fromtimestamp(timestamp, timezone.utc)
                # fixed: forecast dates and rendered times must use the city's offset.
                local_time = sample_time.astimezone(local_timezone)
                days.setdefault(local_time.date(), []).append((local_time, sample))
        except (KeyError, TypeError, ValueError, OverflowError, OSError):
            raise WeatherError(
                "The weather service returned invalid forecast dates or timezone."
            ) from None
        if not days:
            raise WeatherError("The weather service returned empty forecast data.")

        forecast_data = []
        for date in sorted(days)[:5]:
            samples = days[date]
            noon = samples[0][0].replace(hour=12, minute=0, second=0, microsecond=0)
            local_time, sample = min(
                samples,
                key=lambda entry: (abs((entry[0] - noon).total_seconds()), entry[0]),
            )
            main = sample["main"]
            weather = sample["weather"][0]
            forecast_data.append(
                {
                    "dt_txt": local_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "temp": main["temp"],
                    "feels_like_temp": main["feels_like"],
                    "humidity": main["humidity"],
                    "main": weather["main"],
                    "description": weather["description"],
                    "id": weather["id"],
                    "icon": weather["icon"],
                    "wind_speed": sample["wind"]["speed"],
                    "temp_min": min(
                        entry["main"].get("temp_min", entry["main"]["temp"])
                        for _, entry in samples
                    ),
                    "temp_max": max(
                        entry["main"].get("temp_max", entry["main"]["temp"])
                        for _, entry in samples
                    ),
                }
            )
        return forecast_data
