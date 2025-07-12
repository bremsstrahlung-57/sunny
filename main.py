import os
import json
import requests
import argparse
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
api_url = f"http://api.openweathermap.org/data/2.5/forecast?id=524901&appid={api_key}"

CITY_NAME = "Delhi"
COUNTRY_CODE = "IN"


def get_weather_by_city(city: str, country: str):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"


weather_delhi = get_weather_by_city(CITY_NAME, COUNTRY_CODE)
temperature = weather_delhi["main"]["temp"]
humidity = weather_delhi["main"]["humidity"]
description = weather_delhi["weather"][0]["description"]

# print(f"{CITY_NAME}")
# print(f"Temperature: {temperature}°C")
# print(f"Humidity: {humidity}%")
# print(f"Description: {description}")

parser = argparse.ArgumentParser(description="fetch weather")

parser.add_argument("city", help="city name")
parser.add_argument("-t", "--temp", help="only temp of the city", action="store_true")

args = parser.parse_args()

wea = f"{args.city}\n"

if args.temp:
    wea += f"\nTemp: {temperature}"
else:
    wea += f"{weather_delhi}"
print(wea)