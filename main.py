from utility import Weather
from configure import ConfigManager
from importlib.metadata import version

import sys
import argparse
from rich.console import Console
from rich import print, box
from rich.panel import Panel
from rich.columns import Columns

# TODO: Add a flag like --ascii or make ASCII art auto-show by default.
# TODO: Add a --theme option for different output styles (minimal, detailed, fun, etc.)


WEATHER = Weather()
CONSOLE = Console()
CONFIG = ConfigManager()


def main():
    API_KEY = CONFIG.get_api_key
    DEFAULT_LOCATION = CONFIG.get_location
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

    UNIT = CONFIG.get_unit
    DEG = "°C"
    WIND_SPEED_UNIT = "m/s"
    if args.units:
        UNIT = args.units.lower()
        DEG = "°F" if UNIT == "imperial" else "°C"
        WIND_SPEED_UNIT = "mi/h" if UNIT == "imperial" else "m/s"

    city = args.city if args.city else DEFAULT_LOCATION

    if not city:
        print(
            f"[bold red]Error[/bold red]: City name not provided [underline]{CONFIG.config_file_location}[/underline]"
        )
        sys.exit(1)

    if args.version:
        print(f"{version("sunny")}")
        return

    if args.about:
        print(f"[bold yellow]sunny[/bold yellow] - a minimal cli weather tool")
        return
    
    if args.city:
        if "_" in args.city:
            args.city = args.city.replace("_", "%20")
        DEFAULT_LOCATION = args.city

    if (args.city and not (args.temp or args.humidity or args.description)) or len(
        sys.argv
    ) == 1:
        weather = WEATHER.get_weather_city_json(DEFAULT_LOCATION, UNIT)
        DEFAULT_LOCATION = DEFAULT_LOCATION.replace("%20", " ")

        try:
            temperature = weather["main"]["temp"]
            feels_like_temp = weather["main"]["feels_like"]
            humidity = weather["main"]["humidity"]
            desc = weather["weather"][0]["description"]
            cond = weather["weather"][0]["main"]
            wind = weather["wind"]["speed"]
            ASCII_WEATHER = f"[{CONFIG.condition_colour(cond)}]{CONFIG.ascii_art(cond, weather["weather"][0]["icon"])}[/{CONFIG.condition_colour(cond)}]"

            content = Columns(
                [
                    Panel(
                        f"[{CONFIG.condition_colour(cond)}]{desc.capitalize()}[/{CONFIG.condition_colour(cond)}]",
                        box=box.MINIMAL,
                    ),
                    Panel(
                        f"[{CONFIG.temp_colour(temperature)}]Temp: {temperature:.2f}({feels_like_temp:.2f}){DEG}[/{CONFIG.temp_colour(temperature)}]",
                        box=box.MINIMAL,
                    ),
                    Panel(
                        f"[{CONFIG.humid_colour(humidity)}]Humidity: {humidity}[/{CONFIG.humid_colour(humidity)}]",
                        box=box.MINIMAL,
                    ),
                    Panel(
                        f"[{CONFIG.wind_colour()}]Wind: {wind}{WIND_SPEED_UNIT}[/{CONFIG.wind_colour()}]",
                        box=box.MINIMAL,
                    ),
                ]
            )

            PANEL = Panel(
                content,
                title=f"[{CONFIG.city_colour()}]{DEFAULT_LOCATION.capitalize()}[/{CONFIG.city_colour()}]",
                border_style=f"bold {CONFIG.city_colour()}",
                box=box.ROUNDED,
                padding=(0, 0),
                width=50,
                subtitle=f"Coord: {weather["coord"]["lon"], weather["coord"]["lat"]} Country: {weather["sys"]["country"]}",
            )

            ASCII_PANEL = Panel(
                ASCII_WEATHER,
                box=box.MINIMAL,
                padding=(0, 8),
                width=50,
            )

            CONSOLE.print(ASCII_PANEL)
            CONSOLE.print(PANEL)

        except TypeError:
            print(f"{weather}")
            sys.exit(1)

    if args.temp:
        temperature = WEATHER.fetch_temp(DEFAULT_LOCATION, UNIT)
        print(DEFAULT_LOCATION)
        print(
            f"[{CONFIG.temp_colour(temperature)}]Temp:{temperature}{DEG}[/{CONFIG.temp_colour(temperature)}]"
        )

    if args.humidity:
        humidity = WEATHER.fetch_humid(DEFAULT_LOCATION, UNIT)
        print(
            f"[{CONFIG.humid_colour(humidity)}]Humidity: {humidity}[/{CONFIG.humid_colour(humidity)}]"
        )

    if args.description:
        description = WEATHER.fetch_desc(DEFAULT_LOCATION, UNIT)
        print(
            f"[{CONFIG.condition_colour(args.description)}]{description}[/{CONFIG.condition_colour(args.description)}]"
        )


if __name__ == "__main__":
    main()
