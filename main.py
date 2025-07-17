from utility import Weather
from configure import get_api_key, get_city_name, get_unit, config_file_location
from importlib.metadata import version

import sys
import json
import argparse

WEATHER = Weather()

# FIXME: Location with space in their having error in API calls.


def main():
    API_KEY = get_api_key()
    DEFAULT_LOCATION = get_city_name()
    # FORECAST_URL = (
    #     f"http://api.openweathermap.org/data/2.5/forecast?id=524901&appid={API_KEY}"
    # )

    if not API_KEY:
        print("Error: API key not configured (config.json)")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="fetch weather")

    parser.add_argument("-v", "--version", help="version", action="store_true")
    parser.add_argument("-a", "--about", help="about", action="store_true")
    parser.add_argument("-c", "--city", help="city name (add '_' if city has space)")
    parser.add_argument("-t", "--temp", help="fetch temperature", action="store_true")
    parser.add_argument("-y", "--humidity", help="fetch humditity", action="store_true")
    parser.add_argument("-d", "--description", help="description", action="store_true")
    parser.add_argument("-u", "--units", help="units - `metric` or `imperial`")

    args = parser.parse_args()

    UNIT = get_unit()
    DEG = "°C"
    if args.units:
        UNIT = args.units.lower()
        DEG = "°F" if UNIT == "imperial" else "°C"

    city = args.city if args.city else DEFAULT_LOCATION

    if not city:
        print(f"Error: City name not provided {config_file_location}")
        sys.exit(1)

    if args.version:
        print(f"{version("sunny")}")
        return

    if args.about:
        print(f"sunny - a minimal cli weather tool")
        return

    if (args.city and not (args.temp or args.humidity or args.description)) or len(
        sys.argv
    ) == 1:
        if args.city:
            if "_" in args.city:
                args.city = args.city.replace("_", "%20")
            DEFAULT_LOCATION = args.city

        weather = WEATHER.get_weather_city_json(DEFAULT_LOCATION, UNIT)
        DEFAULT_LOCATION = DEFAULT_LOCATION.replace("%20", " ")

        try:
            temperature = weather["main"]["temp"]
            humidity = weather["main"]["humidity"]
            desc = weather["weather"][0]["description"]
            print(
                f"City: {DEFAULT_LOCATION.capitalize()}\nTemp: {temperature:.2f} {DEG}\nHumidity: {humidity}\n{desc.capitalize()}"
            )
        except TypeError:
            print(f"{weather}")
            sys.exit(1)

    if args.temp:
        print(f"Temp: {WEATHER.fetch_temp(DEFAULT_LOCATION, UNIT)} {DEG}")

    if args.humidity:
        print(f"Humidity: {WEATHER.fetch_humid(DEFAULT_LOCATION, UNIT)}")

    if args.description:
        print(f"Description: {WEATHER.fetch_desc(DEFAULT_LOCATION, UNIT)}")


if __name__ == "__main__":
    main()
