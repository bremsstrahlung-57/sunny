import toml
from rich import box, print
from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text

from sunny.configure import ConfigManager


def show_all_themes():
    """Shows a preview of all themes without creating configuration files."""
    console = Console()
    config = ConfigManager()
    theme_files = sorted(f for f in config.THEMES_DIR.glob("*.toml") if f.is_file())
    themes = {}
    if theme_files:
        for theme_file in theme_files:
            try:
                with theme_file.open("r", encoding="utf-8") as f:
                    themes[theme_file.stem] = toml.load(f)
            except (OSError, toml.TomlDecodeError) as e:
                console.print(
                    f"Warning: Skipping theme {theme_file}: {e}", markup=False
                )
    else:
        themes = {
            name: toml.loads(template) for name, template in config.THEMES.items()
        }

    for name, theme in themes.items():
        theme = config._merge_theme(theme)
        theme_name = name.capitalize()
        panel_config = theme.get("panel", {})
        border_style = panel_config.get("border_style", "bold")
        box_attr = getattr(
            box, str(panel_config.get("box", "ROUNDED")).upper(), box.ROUNDED
        )
        if not isinstance(box_attr, box.Box):
            box_attr = box.ROUNDED
        border_colour = panel_config.get("border_colour", "light_steel_blue")
        width = min(int(panel_config.get("width", 55)), console.width)
        colours = theme["colours"]
        content = Group(
            Text("Thunderstorm", style=colours["col_desc"]["Thunderstorm"]),
            Text("Temp: 25(26) C", style=colours["col_temp"]["mid"]),
            Text("Humidity: 65%", style=colours["col_humid"]["high"]),
            Text("Wind: 3 m/s", style=colours["col_wind"]),
        )
        # fixed: Natural height keeps wrapped preview text from being clipped.
        panel = Panel(
            content,
            title=Text(theme_name, style=colours["col_city"]),
            border_style=f"{border_style} {border_colour}",
            box=box_attr,
            padding=(1, 1),
            width=width,
            subtitle=Text("Coord: (75.00, 32.00) Country: IN"),
        )
        console.print(panel)
        console.print()


def show_all_ascii():
    """Shows a preview of all ascii arts of weather conditions."""
    config = ConfigManager()
    previews = (
        ("Thunderstorm", "Thunderstorm", "11d"),
        ("Drizzle", "Drizzle", "09d"),
        ("Rain", "Rain", "10d"),
        ("Snow", "Snow", "13d"),
        ("Atmosphere", "Atmosphere", "50d"),
        ("Clear Day", "Clear", "01d"),
        ("Clear Night", "Clear", "01n"),
        ("Few Clouds Day", "Clouds", "02d"),
        ("Few Clouds Night", "Clouds", "02n"),
        ("Scattered Clouds", "Clouds", "03n"),
        ("Overcast Clouds", "Clouds", "04n"),
    )
    # fixed: Reuse the art without config I/O or Python 3.12-only f-string syntax.
    for index, (name, condition, icon) in enumerate(previews, 1):
        if index > 1:
            print()
        print(f"{index}. {name}")
        print(config.ascii_art(condition, icon))
