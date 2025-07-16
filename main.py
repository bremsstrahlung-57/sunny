from utility import Weather

import os
import json
import requests
import argparse
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv("API_KEY")
FORECAST_URL = (
    f"http://api.openweathermap.org/data/2.5/forecast?id=524901&appid={API_KEY}"
)
WEATHER = Weather()
CITY_NAME = "Delhi"
COUNTRY_CODE = "IN"
UNIT = "metric"
VERSION = "v0.0.1 -a"

parser = argparse.ArgumentParser(description="fetch weather")

parser.add_argument("-v", "--version", help="version", action="store_true")
parser.add_argument("-a", "--about", help="about", action="store_true")
parser.add_argument("-c", "--city", help="city name")
parser.add_argument("-t", "--temp", help="fetch temperature", action="store_true")
parser.add_argument("-y", "--humidity", help="fetch humditity", action="store_true")
parser.add_argument("-d", "--description", help="description", action="store_true")
parser.add_argument("-u", "--units", help="units - `metric` or `imperial`")

args = parser.parse_args()


if args.city:
    # weather = WEATHER.get_weather_city_json(args.city, args.units)
    # json_data = json.dumps(weather, indent=4)

    if args.units:
        UNIT = args.units

    CITY_NAME = args.city
    temperature = WEATHER.fetch_temp(CITY_NAME, UNIT)
    humidity = WEATHER.fetch_humid(CITY_NAME, UNIT)
    desc = WEATHER.fetch_desc(CITY_NAME, UNIT)

    print(
        f"City: {CITY_NAME.capitalize()}\nTemp: {temperature}\nHumidity: {humidity}\n{desc.capitalize()}"
    )

if args.temp:
    print(f"Temp: {WEATHER.fetch_temp(CITY_NAME, UNIT)}")

if args.humidity:
    print(f"Humidity: {WEATHER.fetch_humid(CITY_NAME, UNIT)}")

if args.description:
    print(f"Description: {WEATHER.fetch_desc(CITY_NAME, UNIT)}")

if args.version:
    print(f"{VERSION}")

if args.about:
    print(f"sunny - a minimal cli weather tool")
