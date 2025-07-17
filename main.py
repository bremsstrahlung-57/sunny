from utility import Weather
from configure import get_api_key, get_city_name, get_unit, config_file_location
from configure import temp_colour, humid_colour, desc_colour, city_colour
from importlib.metadata import version

import sys
import argparse
from rich import print

WEATHER = Weather()


def main():
    API_KEY = get_api_key()
    DEFAULT_LOCATION = get_city_name()
    # FORECAST_URL = (
    #     f"http://api.openweathermap.org/data/2.5/forecast?id=524901&appid={API_KEY}"
    # )

    if not API_KEY:
        print("[bold red]Error[/bold red]: API key not configured (config.json)")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="see weather in cli")

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
        print(
            f"[bold red]Error[/bold red]: City name not provided [underline]{config_file_location}[/underline]"
        )
        sys.exit(1)

    if args.version:
        print(f"{version("sunny")}")
        return

    if args.about:
        print(f"[bold yellow]sunny[/bold yellow] - a minimal cli weather tool")
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
                f"[{city_colour()}]City: {DEFAULT_LOCATION.capitalize()}[/{city_colour()}]\n[{temp_colour(temperature)}]Temp: {temperature:.2f} {DEG}[/{temp_colour(temperature)}]\n[{humid_colour(humidity)}]Humidity: {humidity}[/{humid_colour(humidity)}]\n[{desc_colour(weather["weather"][0]["main"])}]{desc.capitalize()}[/{desc_colour(weather["weather"][0]["main"])}]"
            )
        except TypeError:
            print(f"{weather}")
            sys.exit(1)

    if args.temp:
        temperature = WEATHER.fetch_temp(DEFAULT_LOCATION, UNIT)
        print(
            f"[{temp_colour(temperature)}]Temp:{temperature} {DEG}[/{temp_colour(temperature)}]"
        )

    if args.humidity:
        humidity = WEATHER.fetch_humid(DEFAULT_LOCATION, UNIT)
        print(
            f"[{humid_colour(humidity)}]Humidity: {humidity}[/{humid_colour(humidity)}]"
        )

    if args.description:
        description = WEATHER.fetch_desc(DEFAULT_LOCATION, UNIT)
        print(
            f"[{desc_colour(description)}]Description: {WEATHER.fetch_desc(DEFAULT_LOCATION, UNIT)}[/{desc_colour(description)}]"
        )


if __name__ == "__main__":
    main()
