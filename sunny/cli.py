from sunny.utility import Weather
from sunny.configure import ConfigManager
from sunny.themes import show_all_ascii, show_all_themes

import os
import sys
import argparse
from datetime import datetime
from typing import Dict, Any, Optional
from rich.console import Console
from rich import print, box
from rich.panel import Panel
from rich.columns import Columns
from importlib.metadata import version


class WeatherCLI:
    """Main Weather CLI application class"""

    def __init__(self):
        self.weather = Weather()
        self.console = Console()
        self.config = ConfigManager()

    def setup_argument_parser(self) -> argparse.ArgumentParser:
        """Setup and configure argument parser"""
        parser = argparse.ArgumentParser(description="See weather in CLI", prog="sunny")

        parser.add_argument("-v", "--version", help="Show version", action="store_true")
        parser.add_argument(
            "-a", "--about", help="Show about information", action="store_true"
        )
        parser.add_argument(
            "-c", "--city", help="City name (add '_' if city has space)"
        )
        parser.add_argument(
            "-t", "--temp", help="Fetch temperature only", action="store_true"
        )
        parser.add_argument(
            "-y", "--humidity", help="Fetch humidity only", action="store_true"
        )
        parser.add_argument(
            "-d",
            "--description",
            help="Fetch weather description only",
            action="store_true",
        )
        parser.add_argument(
            "-u",
            "--units",
            choices=["metric", "imperial"],
            help="Temperature units - 'metric' or 'imperial'",
        )
        parser.add_argument(
            "--ascii", help="Show ascii art of weather condition`", action="store_true"
        )
        parser.add_argument(
            "--forecast", help="Show weather forecast of 5 days`", action="store_true"
        )
        parser.add_argument(
            "--showall",
            help="Show all available ASCII art`",
            action="store_true",
        )
        parser.add_argument(
            "--themes", help="Show all available themes`", action="store_true"
        )
        parser.add_argument(
            "--init", help="Initialise config files", action="store_true"
        )

        return parser

    def validate_config(self) -> tuple[str, str]:
        """Validate configuration and return API key and default location."""
        if not os.path.exists(self.config.config_file_location):
            print(
                "[bold red]Error[/bold red]: Config file not found. Run '--init' to setup configuration"
            )
            sys.exit(1)

        api_key = self.config.get_api_key
        if not api_key:
            print(
                f"[bold red]Error[/bold red]: API key not configured. Check {self.config.config_file_location}"
            )
            sys.exit(1)

        default_location = self.config.get_location
        return api_key, default_location

    def get_version(self) -> str:
        return version("sunny")

    def get_temperature_units(self, args_units: Optional[str]) -> tuple[str, str, str]:
        """Get temperature units and symbols"""
        unit = args_units.lower() if args_units else self.config.get_unit

        if unit == "imperial":
            return unit, "°F", "mi/h"
        else:
            return unit, "°C", "m/s"

    def process_city_name(self, city_name: str) -> str:
        return city_name.replace("_", "%20") if "_" in city_name else city_name

    def get_weather_data(self, location: str, unit: str) -> Dict[str, Any]:
        """Get weather data"""
        try:
            return self.weather.get_weather_city_json(location, unit)
        except Exception as e:
            print(
                f"[bold red]Error[/bold red]: Failed to fetch weather data - {str(e)}"
            )
            sys.exit(1)

    def display_ascii_art(self, weather_data: Dict[str, Any]) -> None:
        """Display ASCII art for weather condition"""
        condition = weather_data["weather"][0]["main"]
        icon = weather_data["weather"][0]["icon"]
        color = self.config.condition_colour(condition)
        ascii_art = f"[{color}]{self.config.ascii_art(condition, icon)}[/{color}]"
        print(ascii_art)

    def display_full_weather(
        self,
        weather_data: Dict[str, Any],
        location: str,
        deg_symbol: str,
        wind_unit: str,
    ) -> None:
        """Display complete weather information."""
        try:
            main_data = weather_data["main"]
            weather_info = weather_data["weather"][0]
            wind_data = weather_data["wind"]
            coord_data = weather_data["coord"]
            sys_data = weather_data["sys"]

            temperature = main_data["temp"]
            feels_like_temp = main_data["feels_like"]
            humidity = main_data["humidity"]
            description = weather_info["description"]
            condition = weather_info["main"]
            wind_speed = wind_data["speed"]

            ascii_color = self.config.condition_colour(condition)
            ascii_art = f"[{ascii_color}]{self.config.ascii_art(condition, weather_info['icon'])}[/{ascii_color}]"

            content_panels = [
                Panel(
                    f"[{self.config.condition_colour(condition)}]{description.capitalize()}[/{self.config.condition_colour(condition)}]",
                    box=box.MINIMAL,
                ),
                Panel(
                    f"[{self.config.temp_colour(temperature)}]Temp: {temperature:.1f}° (feels {feels_like_temp:.1f}°) {deg_symbol}[/{self.config.temp_colour(temperature)}]",
                    box=box.MINIMAL,
                ),
                Panel(
                    f"[{self.config.humid_colour(humidity)}]Humidity: {humidity}%[/{self.config.humid_colour(humidity)}]",
                    box=box.MINIMAL,
                ),
                Panel(
                    f"[{self.config.wind_colour}]Wind: {wind_speed} {wind_unit}[/{self.config.wind_colour}]",
                    box=box.MINIMAL,
                ),
            ]

            content = Columns(content_panels)

            weather_panel = Panel(
                content,
                title=f"[{self.config.city_colour}]{location.replace('%20', ' ').title()}[/{self.config.city_colour}]",
                border_style=f"{self.config.get_panel_attribute('border_style')} {self.config.get_panel_attribute('border_colour')}",
                box=self.config.get_box_style(),
                padding=(
                    self.config.get_panel_attribute("padding_top_right"),
                    self.config.get_panel_attribute("padding_bottom_left"),
                ),
                width=self.config.get_panel_attribute("width"),
                height=self.config.get_panel_attribute("height"),
                subtitle=f"[dim]Coord: ({coord_data['lon']:.2f}, {coord_data['lat']:.2f}) | Country: {sys_data['country']}[/dim]",
            )

            ascii_panel = Panel(
                ascii_art,
                border_style=f"{self.config.get_ascii_panel_attribute('border_style')} {self.config.city_colour}",
                box=self.config.get_ascii_box_style(),
                padding=(
                    self.config.get_ascii_panel_attribute("padding_top_right"),
                    self.config.get_ascii_panel_attribute("padding_bottom_left"),
                ),
                width=self.config.get_ascii_panel_attribute("width"),
                height=self.config.get_ascii_panel_attribute("height"),
            )

            self.console.print(ascii_panel)
            self.console.print(weather_panel)

        except (KeyError, TypeError) as e:
            print(f"[bold red]Error[/bold red]: Invalid weather data format - {e}")
            sys.exit(1)

    def display_forecast(
        self,
        location: str,
        weather_data: list,
        deg_symbol: str,
        wind_unit: str,
    ):
        """Display 5-days forecast."""

        try:
            day_cards = []
            for i in range(5):

                dt_text = weather_data[i].get("dt_txt")
                dt = datetime.strptime(dt_text, "%Y-%m-%d %H:%M:%S")
                day_str = dt.strftime("%a %d %b")
                time_str = dt.strftime("%I:%M %p")

                temperature = weather_data[i].get("temp")
                feels_like_temp = weather_data[i].get("feels_like_temp")
                humidity = weather_data[i].get("humidity")
                description = weather_data[i].get("description")
                condition = weather_data[i].get("main")
                wind_speed = weather_data[i].get("wind_speed")
                icon = weather_data[i].get("icon")

                ascii_color = self.config.condition_colour(condition)
                ascii_art = f"[{ascii_color}]{self.config.ascii_art(condition,icon )}[/{ascii_color}]"

                details = "\n".join(
                    [
                        f"[{self.config.condition_colour(condition)}]{description.capitalize()}[/{self.config.condition_colour(condition)}]",
                        f"[{self.config.temp_colour(temperature)}]Temp: {temperature:.1f}° (feels {feels_like_temp:.1f}°) {deg_symbol}[/{self.config.temp_colour(temperature)}]",
                        f"[{self.config.humid_colour(humidity)}]Humidity: {humidity}%[/{self.config.humid_colour(humidity)}]",
                        f"[{self.config.wind_colour}]Wind: {wind_speed} {wind_unit}[/{self.config.wind_colour}]",
                    ]
                )

                card = Panel(
                    f"{ascii_art}\n\n{details}",
                    title=f"[{self.config.city_colour}]{day_str}[/{self.config.city_colour}]",
                    subtitle=f"[dim]{time_str}[/dim]",
                    border_style=f"{self.config.get_panel_attribute('border_style')} {self.config.get_panel_attribute('border_colour')}",
                    box=self.config.get_box_style(),
                    padding=(1,4),
                    width=30,
                    height=20,
                )

                day_cards.append(card)

            self.console.print(Columns(day_cards, expand=True))

        except (KeyError, TypeError) as e:
            print(f"[bold red]Error[/bold red]: Invalid weather data format - {e}")
            sys.exit(1)

    def display_temperature_only(
        self, location: str, unit: str, deg_symbol: str
    ) -> None:
        """Display only temperature information"""
        try:
            temperature = self.weather.fetch_temp(location, unit)
            color = self.config.temp_colour(temperature)
            print(f"[{color}]Temperature: {temperature:.1f}{deg_symbol}[/{color}]")
        except Exception as e:
            print(f"[bold red]Error[/bold red]: Failed to fetch temperature - {str(e)}")
            sys.exit(1)

    def display_humidity_only(self, location: str, unit: str) -> None:
        """Display only humidity information"""
        try:
            humidity = self.weather.fetch_humid(location, unit)
            color = self.config.humid_colour(humidity)
            print(f"[{color}]Humidity: {humidity}%[/{color}]")
        except Exception as e:
            print(f"[bold red]Error[/bold red]: Failed to fetch humidity - {str(e)}")
            sys.exit(1)

    def display_description_only(self, location: str, unit: str) -> None:
        """Display only weather description."""
        try:
            weather_data = self.get_weather_data(location, unit)
            description = weather_data["weather"][0]["description"]
            condition = weather_data["weather"][0]["main"]
            color = self.config.condition_colour(condition)
            print(f"[{color}]{description.capitalize()}[/{color}]")
        except Exception as e:
            print(f"[bold red]Error[/bold red]: Failed to fetch description - {str(e)}")
            sys.exit(1)

    def run(self) -> None:
        """Main application entry point"""
        parser = self.setup_argument_parser()
        args = parser.parse_args()

        if args.init:
            self.config.setup_config()
            print("[bold green]Configuration initialized successfully![/bold green]")
            return

        if args.about:
            print("[bold yellow]sunny[/bold yellow] - A minimal CLI weather tool")
            return

        if args.showall:
            show_all_ascii()
            return

        if args.themes:
            print()
            show_all_themes()
            return

        if args.version:
            version = self.get_version()
            print(f"[bold green]{version}[/bold green]")

        api_key, default_location = self.validate_config()

        location = self.process_city_name(args.city) if args.city else default_location
        if not location:
            print(
                f"[bold red]Error[/bold red]: No city specified. Configure default location in {self.config.config_file_location}"
            )
            sys.exit(1)

        unit, deg_symbol, wind_unit = self.get_temperature_units(args.units)

        if args.temp:
            self.display_temperature_only(location, unit, deg_symbol)

        if args.humidity:
            self.display_humidity_only(location, unit)

        if args.description:
            self.display_description_only(location, unit)

        if args.ascii:
            weather_data = self.get_weather_data(location, unit)
            self.display_ascii_art(weather_data)

            if args.city and not (args.temp or args.humidity or args.description):
                return

        if (
            not any([args.temp, args.humidity, args.description, args.forecast])
            or len(sys.argv) == 1
        ):
            weather_data = self.get_weather_data(location, unit)
            self.display_full_weather(weather_data, location, deg_symbol, wind_unit)
        else:
            data = self.weather.fetch_forecast(location, unit)
            self.display_forecast(location, data, deg_symbol, wind_unit)
