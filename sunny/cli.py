import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from importlib.metadata import version
from textwrap import dedent
from typing import Any, Dict, Optional

from rich.align import Align
from rich.columns import Columns
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from sunny.configure import ConfigManager
from sunny.themes import show_all_ascii, show_all_themes
from sunny.utility import Weather


class WeatherCLI:
    """Main Weather CLI application class."""

    def __init__(self):
        self.weather = Weather()
        self.console = Console()
        self.config = ConfigManager()

    def setup_argument_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description="See weather in CLI", prog="sunny")
        parser.add_argument("-v", "--version", help="Show version", action="store_true")
        parser.add_argument(
            "-a", "--about", help="Show about information", action="store_true"
        )
        parser.add_argument(
            "-c", "--city", help="City name (quote spaces or use underscores)"
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
            help="Temperature unit system",
        )
        parser.add_argument(
            "--ascii", help="Show weather ASCII art only", action="store_true"
        )
        parser.add_argument(
            "--forecast", help="Show up to 5 days of forecast", action="store_true"
        )
        parser.add_argument(
            "--showall", help="Preview all ASCII art", action="store_true"
        )
        parser.add_argument(
            "--themes", help="Preview available themes", action="store_true"
        )
        parser.add_argument(
            "--init", help="Initialize missing config files", action="store_true"
        )
        return parser

    def validate_config(self) -> tuple[str, str]:
        api_key = self.config.get_api_key
        if not api_key:
            raise ValueError(
                f"API key not configured. Add your OpenWeather API key to "
                f"{self.config.config_file_location}"
            )
        return api_key, self.config.get_location

    def get_version(self) -> str:
        return version("sunny")

    def get_temperature_units(self, args_units: Optional[str]) -> tuple[str, str, str]:
        unit = args_units.lower() if args_units else self.config.get_unit
        return (unit, "°F", "mi/h") if unit == "imperial" else (unit, "°C", "m/s")

    def process_city_name(self, city_name: str) -> str:
        return city_name.replace("_", " ").strip()

    def get_weather_data(self, location: str, unit: str) -> Dict[str, Any]:
        return self.weather.get_weather_city_json(location, unit)

    def _weather_art(self, condition: str, icon: str) -> Text:
        art = dedent(self.config.ascii_art(condition, icon)).strip("\n")
        return Text(
            "\n".join(line.rstrip() for line in art.splitlines()),
            style=self.config.condition_colour(condition),
            no_wrap=True,
        )

    def display_ascii_art(self, weather_data: Dict[str, Any]) -> None:
        weather = weather_data["weather"][0]
        self.console.print(self._weather_art(weather["main"], weather["icon"]))

    def display_full_weather(
        self,
        weather_data: Dict[str, Any],
        location: str,
        deg_symbol: str,
        wind_unit: str,
    ) -> None:
        main = weather_data["main"]
        weather = weather_data["weather"][0]
        condition_color = self.config.condition_colour(weather["main"])
        unit = "imperial" if deg_symbol == "°F" else "metric"
        temperature_color = self.config.temp_colour(main["temp"], unit)
        art = self._weather_art(weather["main"], weather["icon"])
        details = Group(
            Text(weather["description"].capitalize(), style=condition_color),
            Text(f"{main['temp']:.1f}{deg_symbol}", style=f"bold {temperature_color}"),
            Text(f"Feels like {main['feels_like']:.1f}{deg_symbol}", style="dim"),
            Text(""),
            Text(
                f"Humidity  {main['humidity']:g}%",
                style=self.config.humid_colour(main["humidity"]),
            ),
            Text(
                f"Wind      {weather_data['wind']['speed']:g} {wind_unit}",
                style=self.config.wind_colour,
            ),
        )
        width = min(self.config.get_panel_attribute("width"), self.console.width)
        # fixed: Let narrow layouts grow vertically instead of clipping to theme heights.
        if width >= 58:
            content = Table.grid(padding=(0, 1), expand=True)
            content.add_column(no_wrap=True)
            content.add_column(ratio=1)
            content.add_row(art, details)
        else:
            content = Group(Align.center(art), Text(""), details)
        coords = weather_data["coord"]
        subtitle = Text(
            f"{weather_data['sys']['country']} · {coords['lat']:.2f}, {coords['lon']:.2f}",
            style="dim",
        )
        self.console.print(
            Panel(
                content,
                title=Text(
                    weather_data.get("name") or location, style=self.config.city_colour
                ),
                subtitle=subtitle,
                border_style=(
                    f"{self.config.get_panel_attribute('border_style')} "
                    f"{self.config.get_panel_attribute('border_colour')}"
                ),
                box=self.config.get_box_style(),
                padding=(
                    self.config.get_panel_attribute("padding_top_right"),
                    self.config.get_panel_attribute("padding_bottom_left"),
                ),
                width=width,
            )
        )

    def display_forecast(
        self, location: str, weather_data: list, deg_symbol: str, wind_unit: str
    ) -> None:
        unit = "imperial" if deg_symbol == "°F" else "metric"
        self.console.print(
            Text(
                f"{location} · {len(weather_data)}-day forecast",
                style=self.config.city_colour,
            )
        )
        day_cards = []
        for day in weather_data:
            date = datetime.strptime(day["dt_txt"], "%Y-%m-%d %H:%M:%S")
            condition_color = self.config.condition_colour(day["main"])
            art = self._weather_art(day["main"], day["icon"])
            details = [
                art,
                Text(""),
                Text(day["description"].capitalize(), style=condition_color),
                Text(
                    f"{day['temp']:.1f}{deg_symbol} · feels {day['feels_like_temp']:.1f}{deg_symbol}",
                    style=self.config.temp_colour(day["temp"], unit),
                ),
            ]
            if "temp_min" in day and "temp_max" in day:
                details.append(
                    Text(
                        f"Low {day['temp_min']:.1f}° / High {day['temp_max']:.1f}°",
                        style="dim",
                    )
                )
            details.extend(
                [
                    Text(
                        f"Humidity  {day['humidity']:g}%",
                        style=self.config.humid_colour(day["humidity"]),
                    ),
                    Text(
                        f"Wind      {day['wind_speed']:g} {wind_unit}",
                        style=self.config.wind_colour,
                    ),
                ]
            )
            day_cards.append(
                Panel(
                    Group(*details),
                    title=Text(
                        date.strftime("%a %d %b"), style=self.config.city_colour
                    ),
                    subtitle=Text(f"{date:%H:%M} local", style="dim"),
                    border_style=(
                        f"{self.config.get_panel_attribute('border_style')} "
                        f"{self.config.get_panel_attribute('border_colour')}"
                    ),
                    box=self.config.get_box_style(),
                    padding=(1, 1),
                    width=min(34, self.console.width),
                )
            )
        self.console.print(Columns(day_cards, equal=True, padding=(0, 1)))

    def display_temperature_only(
        self, location: str, unit: str, deg_symbol: str, weather_data=None
    ) -> None:
        data = (
            weather_data
            if weather_data is not None
            else self.get_weather_data(location, unit)
        )
        temperature = data["main"]["temp"]
        self.console.print(
            Text(
                f"Temperature: {temperature:.1f}{deg_symbol}",
                style=self.config.temp_colour(temperature, unit),
            )
        )

    def display_humidity_only(
        self, location: str, unit: str, weather_data=None
    ) -> None:
        data = (
            weather_data
            if weather_data is not None
            else self.get_weather_data(location, unit)
        )
        humidity = data["main"]["humidity"]
        self.console.print(
            Text(f"Humidity: {humidity:g}%", style=self.config.humid_colour(humidity))
        )

    def display_description_only(
        self, location: str, unit: str, weather_data=None
    ) -> None:
        data = (
            weather_data
            if weather_data is not None
            else self.get_weather_data(location, unit)
        )
        weather = data["weather"][0]
        self.console.print(
            Text(
                weather["description"].capitalize(),
                style=self.config.condition_colour(weather["main"]),
            )
        )

    def run(self) -> None:
        parser = self.setup_argument_parser()
        args = parser.parse_args()
        if args.init:
            self.config.setup_config()
            return
        if args.about:
            self.console.print(
                "[bold yellow]sunny[/bold yellow] - A minimal CLI weather tool"
            )
            return
        if args.showall:
            show_all_ascii()
            return
        if args.themes:
            show_all_themes()
            return
        if args.version:
            self.console.print(self.get_version())
            return

        api_key, default_location = self.validate_config()
        location = self.process_city_name(
            args.city if args.city is not None else default_location
        )
        if not location:
            parser.error(
                "No city specified. Use --city or set [defaults].location in your config."
            )
        self.weather.api_key = api_key
        unit, deg_symbol, wind_unit = self.get_temperature_units(args.units)
        selected_output = any((args.temp, args.humidity, args.description, args.ascii))
        full_weather = not selected_output and not args.forecast
        display_config = self.config.config.get("display", {})
        forecast = args.forecast or (
            full_weather and display_config.get("show_forecast", False)
        )
        days = display_config.get("days", 5)
        if forecast and (type(days) is not int or not 1 <= days <= 5):
            raise ValueError("Set [display].days to an integer between 1 and 5.")
        need_current = full_weather or selected_output
        weather_data = None
        forecast_data = None
        with self.console.status("Fetching weather…", spinner="dots"):
            if need_current and forecast:
                # fixed: Independent endpoints run concurrently; selected metrics share one response.
                with ThreadPoolExecutor(max_workers=2) as executor:
                    current_request = executor.submit(
                        self.get_weather_data, location, unit
                    )
                    forecast_request = executor.submit(
                        self.weather.fetch_forecast, location, unit
                    )
                    weather_data = current_request.result()
                    forecast_data = forecast_request.result()
            elif need_current:
                weather_data = self.get_weather_data(location, unit)
            else:
                forecast_data = self.weather.fetch_forecast(location, unit)

        if full_weather:
            self.display_full_weather(weather_data, location, deg_symbol, wind_unit)
        if args.temp:
            self.display_temperature_only(location, unit, deg_symbol, weather_data)
        if args.humidity:
            self.display_humidity_only(location, unit, weather_data)
        if args.description:
            self.display_description_only(location, unit, weather_data)
        if args.ascii:
            self.display_ascii_art(weather_data)
        if forecast:
            self.display_forecast(location, forecast_data[:days], deg_symbol, wind_unit)
