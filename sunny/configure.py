from pathlib import Path

import toml
from platformdirs import user_config_dir
from rich import box, print


class ConfigManager:
    def __init__(self) -> None:
        self.APP_NAME = "sunny"
        self.CONFIG_DIR = Path(user_config_dir(self.APP_NAME))
        self.CONFIG_FILE = self.CONFIG_DIR / "config.toml"
        self.THEMES_DIR = self.CONFIG_DIR / "themes"
        self.THEMES_FILES = [
            self.THEMES_DIR / "sunny_dynamic.toml",
            self.THEMES_DIR / "minimal.toml",
            self.THEMES_DIR / "cyberpunk.toml",
        ]
        self._config_data = None
        self._theme_data = None
        self.DEFAULT_CONFIG = """
# sunny Configuration

# Get your free API key from https://openweathermap.org/api
[api]
key = "YOUR-OPEN-WEATHER-API-KEY"

# Set your default city
[defaults]
location = "Delhi"
units = "metric"

# Default theme to use and forecast
[display]
show_forecast = false
days = 5
theme = "sunny_dynamic"
"""
        self.THEMES = {
            "sunny_dynamic": """
# sunny_dynamic
# Go to Rich documentation to know about values of attributes
[panel]
border_style = "bold"
box = "ROUNDED"
border_colour = "light_steel_blue"
padding_top_right = 1
padding_bottom_left = 1
padding_top = 1
padding_right = 1
padding_bottom = 1
padding_left = 1
width = 60
height = 10

[ascii_panel]
border_style = "bold"
box = "MINIMAL"
border_colour = "light_steel_blue"
padding_top_right = 0
padding_bottom_left = 8
padding_top = 0
padding_right = 0
padding_bottom = 8
padding_left = 8
width = 60
height = 10

[colours]
col_city = "light_steel_blue"
col_wind = "sky_blue1"

[colours.col_temp]
high = "sandy_brown"
mid = "chartreuse3"
low = "deep_sky_blue1"

[colours.col_humid]
high = "cornflower_blue"
mid = "green_yellow"
low = "indian_red"

[colours.col_desc]
Thunderstorm = "dodger_blue2"
Drizzle = "deep_sky_blue2"
Rain = "light_steel_blue3"
Snow = "bright_white"
Atmosphere = "grey53"
Clear = "dark_orange"
Clouds = "orchid"
""",
            "minimal": """
# minimal
# Go to Rich documentation to know about values of attributes
[panel]
border_style = "dim"             
box = "MINIMAL"                  
border_colour = "grey50"         
padding_top_right = 0            
padding_bottom_left = 0          
padding_top = 0                  
padding_right = 0                
padding_bottom = 0               
padding_left = 0                 
width = 60                 
height = 10                     

[ascii_panel]
border_style = "dim"             
box = "ASCII"                    
border_colour = "grey50"         
padding_top_right = 0            
padding_bottom_left = 4          
padding_top = 0                  
padding_right = 0                
padding_bottom = 4               
padding_left = 4                 
width = 60                     
height = 10                      
        
[colours]
col_city = "grey70"              
col_wind = "sky_blue3"           

[colours.col_temp]
high = "orange3"                 
mid = "green3"                   
low = "blue3"                    
        
[colours.col_humid]
high = "steel_blue"              
mid = "lime_green"               
low = "red3"                     
        
[colours.col_desc]
Thunderstorm = "blue4"           
Drizzle = "sky_blue2"            
Rain = "grey62"                  
Snow = "white"                   
Atmosphere = "grey46"            
Clear = "yellow3"                
Clouds = "purple3"  
""",
            "cyberpunk": """
# cyberpunk
# Go to Rich documentation to know about values of attributes
[panel]
border_style = "bold"
box = "HEAVY"
border_colour = "cyan1"
padding_top_right = 1
padding_bottom_left = 1
padding_top = 1
padding_right = 1
padding_bottom = 1
padding_left = 1
width = 60
height = 10

[ascii_panel]
border_style = "bold"
box = "DOUBLE"
border_colour = "magenta2"
padding_top_right = 0
padding_bottom_left = 4
padding_top = 0
padding_right = 0
padding_bottom = 4
padding_left = 4
width = 60
height = 10

[colours]
col_city = "cyan3"
col_wind = "purple2"

[colours.col_temp]
high = "red1"
mid = "yellow1"
low = "blue1"

[colours.col_humid]
high = "deep_pink1"
mid = "green1"
low = "violet"

[colours.col_desc]
Thunderstorm = "deep_sky_blue1"
Drizzle = "cyan2"
Rain = "blue_violet"
Snow = "white"
Atmosphere = "grey27"
Clear = "gold1"
Clouds = "purple3"
""",
        }

    def setup_config(self):
        """Create missing configuration and theme files without replacing user files."""
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        try:
            with self.CONFIG_FILE.open("x", encoding="utf-8") as f:
                f.write(self.DEFAULT_CONFIG)
        except FileExistsError:
            print(f"✅ Configuration exists at: {self.CONFIG_FILE}")
        else:
            print(f"✅ Configuration created at: {self.CONFIG_FILE}")
            print("🛑 Please edit this file to add your OpenWeather API key.")
        self.setup_themes()

    def setup_themes(self):
        """Create each missing built-in theme without replacing user files."""
        self.THEMES_DIR.mkdir(parents=True, exist_ok=True)
        for key, value in self.THEMES.items():
            theme_file = self.THEMES_DIR / f"{key}.toml"
            try:
                with theme_file.open("x", encoding="utf-8") as f:
                    f.write(value)
            except FileExistsError:
                continue
            print(f"✅ Theme {key} created at: {theme_file}")

    def _load_config(self) -> dict:
        """Load configuration data from file."""
        if not self.CONFIG_FILE.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.CONFIG_FILE}. "
                "Run 'sunny --init' to create it, then add your OpenWeather API key."
            )

        try:
            with self.CONFIG_FILE.open("r", encoding="utf-8") as f:
                self._config_data = toml.load(f)
        except toml.TomlDecodeError as e:
            raise ValueError(
                f"Invalid TOML in configuration file {self.CONFIG_FILE}: {e}. "
                "Correct the TOML syntax and try again."
            ) from e
        return self._config_data

    @property
    def config(self) -> dict:
        """Get configuration data, loading it if necessary."""
        if self._config_data is None:
            self._config_data = self._load_config()
        return self._config_data if self._config_data is not None else {}

    @property
    def config_file_location(self) -> Path:
        """Get the configuration file path."""
        return self.CONFIG_FILE

    def get_theme_file(self):
        """Get the theme file path, falling back to sunny_dynamic if needed."""
        theme_name = self.config.get("display", {}).get("theme", "sunny_dynamic")
        theme_file = self.THEMES_DIR / f"{theme_name}.toml"
        if not theme_file.is_file():
            theme_file = self.THEMES_DIR / "sunny_dynamic.toml"
        return str(theme_file)

    def _merge_theme(self, theme_data):
        """Fill missing theme attributes from the built-in default."""
        defaults = toml.loads(self.THEMES["sunny_dynamic"])

        # fixed: Merge nested colour tables so partial themes keep usable defaults.
        def merge(defaults, overrides):
            for key, value in overrides.items():
                if isinstance(value, dict) and isinstance(defaults.get(key), dict):
                    merge(defaults[key], value)
                else:
                    defaults[key] = value

        merge(defaults, theme_data)
        return defaults

    def _load_theme(self):
        """Load a theme with built-in defaults, even when no theme file exists."""
        theme_file = Path(self.get_theme_file())
        if not theme_file.is_file():
            return self._merge_theme({})
        with theme_file.open("r", encoding="utf-8") as f:
            return self._merge_theme(toml.load(f))

    @property
    def theme(self) -> dict:
        """Get theme data, loading it if necessary."""
        if self._theme_data is None:
            self._theme_data = self._load_theme()
        return self._theme_data if self._theme_data is not None else {}

    @property
    def get_api_key(self) -> str:
        """Get API key from config."""
        key = self.config.get("api", {}).get("key", "")
        if not isinstance(key, str):
            raise ValueError(
                f"Invalid API key in {self.CONFIG_FILE}; "
                "set [api].key to a quoted string."
            )
        key = key.strip()
        return "" if key == "YOUR-OPEN-WEATHER-API-KEY" else key

    @property
    def get_location(self) -> str:
        """Get default location from config."""
        location = self.config.get("defaults", {}).get("location", "")
        if not isinstance(location, str):
            raise ValueError(
                f"Invalid location in {self.CONFIG_FILE}; "
                "set [defaults].location to a quoted string."
            )
        return location.strip()

    @property
    def get_unit(self) -> str:
        """Get default units from config."""
        unit = self.config.get("defaults", {}).get("units", "metric")
        if isinstance(unit, str):
            unit = unit.strip().lower()
        if unit not in ("imperial", "metric"):
            raise ValueError(
                f"Invalid units {unit!r} in {self.CONFIG_FILE}; "
                "set [defaults].units to 'imperial' or 'metric'."
            )
        return unit

    @property
    def city_colour(self) -> str:
        """Get city color from theme."""
        file_location = self.get_theme_file()
        try:
            return self.theme.get("colours").get("col_city")
        except Exception as e:
            print(
                f"Warning: No default city color found in {file_location}. Using fallback value 'light_steel_blue'. Exception : {e}"
            )
            return "light_steel_blue"

    def temp_colour(self, temperature: float, units: str = "metric") -> str:
        """Get temperature color using Celsius thresholds for either unit system."""
        if units == "imperial":
            temperature = (temperature - 32) * 5 / 9
        file_location = self.get_theme_file()
        try:
            if temperature > 30:
                return self.theme.get("colours").get("col_temp").get("high")
            elif temperature > 10:
                return self.theme.get("colours").get("col_temp").get("mid")
            else:
                return self.theme.get("colours").get("col_temp").get("low")

        except Exception as e:
            print(
                f"Warning: No default temp color found in {file_location}. Using fallback value 'chartreuse3'. Exception: {e}"
            )
            return "chartreuse3"

    def humid_colour(self, humidity: int) -> str:
        """Get humidity color based on value."""
        file_location = self.get_theme_file()
        try:
            if humidity > 65:
                return self.theme.get("colours").get("col_humid").get("high")
            elif humidity >= 55:
                return self.theme.get("colours").get("col_humid").get("mid")
            else:
                return self.theme.get("colours").get("col_humid").get("low")
        except Exception as e:
            print(
                f"Warning: No default humid color found in {file_location}. Using fallback value 'green_yellow'. Exception: {e}"
            )
            return "green_yellow"

    def condition_colour(self, condition: str):
        """Get weather condition color based on condition type."""
        try:
            if condition == "Thunderstorm":
                return self.theme.get("colours").get("col_desc").get("Thunderstorm")
            elif condition == "Drizzle":
                return self.theme.get("colours").get("col_desc").get("Drizzle")
            elif condition == "Rain":
                return self.theme.get("colours").get("col_desc").get("Rain")
            elif condition == "Snow":
                return self.theme.get("colours").get("col_desc").get("Snow")
            elif condition == "Atmosphere":
                return self.theme.get("colours").get("col_desc").get("Atmosphere")
            elif condition == "Clear":
                return self.theme.get("colours").get("col_desc").get("Clear")
            elif condition == "Clouds":
                return self.theme.get("colours").get("col_desc").get("Clouds")
            else:
                return "dark_orange"
        except Exception as e:
            print(
                f"Warning: No default condition color found in {self.get_theme_file()}. Using fallback value 'dark_orange'. Exception: {e}"
            )
            return "dark_orange"

    @property
    def wind_colour(self) -> str:
        """Get wind color from theme."""
        try:
            return self.theme.get("colours").get("col_wind")
        except Exception as e:
            print(
                f"Warning: No default wind color found in {self.get_theme_file()}. Using fallback value 'sky_blue1'. Exception: {e}"
            )
            return "sky_blue1"

    def ascii_art(self, condition: str, icon: str):
        if condition == "Thunderstorm":
            return r"""                    
           #####            
      ....=########         
    .......:########        
   ............-######      
 ...............*######     
...................*##          
  ...:==+-........          
      ==                    
     =="""
        elif condition == "Drizzle":
            return r"""       
        #####           
   ......*######        
   .........+#####      
.............:*###      
...............         
  ...#........          
    #### #              
      # ##"""
        elif condition == "Rain":
            return r"""
      . =======        
   .....:+======       
  ..........+===       
.............:++       
...............        
 ...++........         
    # ## #             
     ## #"""
        elif condition == "Snow":
            return r"""
               __##____    
  *        *  /  ##  ****  
             /        **** 
   *        /        ******
           /___________****
            |            **
        *   | ___        | 
  *         | | |   ___  | 
            | |_|   | |  **"""
        elif condition == "Atmosphere":
            return r"""
     ######             
  ##########            
     #############      
#############           
   #############        
     ########"""
        elif condition == "Clear":
            if icon == "01d":
                return r"""
   ========           
 ============         
==============        
===============       
===============       
==============        
 ============+        
   ========+"""
            else:
                return r"""         
   ########           
 ############         
##############        
###############       
###############       
##############        
 #############        
   #########"""
        elif condition == "Clouds":
            if icon == "02d":
                return r"""                                    
      ....+========      
    .......=========     
    ...........=====     
 ..............-+===     
...................      
  ................"""
            elif icon == "02n":
                return r"""
           ###         
      ....#########      
    .......#########     
    ..........:#####     
 ..............+####        
  ............"""
            elif icon == "03n":
                return r"""
     .....              
    ........            
  .............         
..................      
..................      
 ................."""
            elif icon == "04n":
                return r"""
           ##            
      .. ######          
    ......+#######       
   ..........:######     
..............-######    
.................*##     
..................       
 ................"""
            else:
                return r"""
     .....              
    ........            
  .............         
..................      
..................      
 ................."""

        else:
            return r"""                                      
      ....+======      
    .......========     
   .............====              
...................=     
  ................"""

    def get_panel_attribute(self, key):
        return self.theme.get("panel", {}).get(key)

    def get_box_style(self):
        box_style = self.theme.get("panel", {}).get("box", "ROUNDED")
        box_object = getattr(box, str(box_style).upper(), box.ROUNDED)
        return box_object if isinstance(box_object, box.Box) else box.ROUNDED

    def get_ascii_panel_attribute(self, key):
        return self.theme.get("ascii_panel", {}).get(key)

    def get_ascii_box_style(self):
        box_style = self.theme.get("ascii_panel", {}).get("box", "ROUNDED")
        box_object = getattr(box, str(box_style).upper(), box.ROUNDED)
        return box_object if isinstance(box_object, box.Box) else box.ROUNDED
