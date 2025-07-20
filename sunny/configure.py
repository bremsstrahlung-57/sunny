import toml
import sys
import os
from pathlib import Path
from importlib.resources import files


class ConfigManager:
    def __init__(self) -> None:
        self.config_dir = files("sunny").joinpath(".config")
        self.theme_dir = self.config_dir.joinpath("themes")
        self.config_file = self.config_dir / "config.toml"
        self.theme_file = None
        self._config_data = None
        self._theme_data = None
        self.user_config_dir = Path.home() / ".config" / "sunny"
        self.user_theme_dir = self.user_config_dir / "themes"

        if (self.user_config_dir / "config.toml").exists():
            self.config_file = self.user_config_dir / "config.toml"
        else:
            self.config_file = self.config_dir / "config.toml"


    def _load_config(self) -> dict:
        """Load configuration data from file."""
        if not self.config_file.exists():
            print(f"Config file not found: {self.config_file}")
            sys.exit(1)
        
        with self.config_file.open("r", encoding="utf-8") as f:
            self._config_data = toml.load(f)
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
        return self.config_file

    def get_theme(self) -> Path:
        """Get the theme file path, falling back to sunny_dynamic if needed."""
        config = self.config

        try:
            display_config = config.get("display", {})
            if not isinstance(display_config, dict):
                display_config = {}
            
            theme_name = display_config.get("theme", "sunny_dynamic")
            theme_path = self.user_theme_dir.joinpath(f"{theme_name}.toml")
            
            if os.path.exists(theme_path):
                self.theme_file = Path(theme_path)
                return self.theme_file
            
            fallback_path = self.theme_dir.joinpath("sunny_dynamic.toml")
            if os.path.exists(fallback_path):
                if theme_name != "sunny_dynamic":
                    print(f"Warning: Theme '{theme_name}' not found, falling back to sunny_dynamic")
                self.theme_file = Path(fallback_path)
                return self.theme_file
            
            raise FileNotFoundError("Neither configured theme nor fallback theme found")

        except (FileNotFoundError, AttributeError, KeyError) as e:
            print(f"Error: Theme file not found or inaccessible: {e}")
            sys.exit(1)

    def _load_theme(self) -> dict:
        """Load theme data from file."""
        theme_file = self.get_theme()
        if not theme_file.exists():
            print(f"Theme file not found: {theme_file}")
            sys.exit(1)
            
        with theme_file.open("r", encoding="utf-8") as f:
            self._theme_data = toml.load(f)
        return self._theme_data

    @property
    def theme(self) -> dict:
        """Get theme data, loading it if necessary."""
        if self._theme_data is None:
            self._theme_data = self._load_theme()
        return self._theme_data if self._theme_data is not None else {}

    @property
    def get_api_key(self) -> str:
        """Get API key from config."""
        config = self.config
        try:
            api_config = config.get("api", {})
            if not isinstance(api_config, dict):
                raise KeyError("Invalid API configuration")
            key = api_config.get("key")
            if not key:
                raise KeyError("API key not found")
            return key
        except (KeyError, TypeError) as e:
            print(f"API key not found in {self.config_file} file: {e}")
            sys.exit(1)

    @property
    def get_location(self) -> str:
        """Get default location from config."""
        config = self.config
        try:
            defaults = config.get("defaults", {})
            if not isinstance(defaults, dict):
                raise KeyError("Invalid defaults configuration")
            location = defaults.get("location")
            if not location:
                raise KeyError("Default location not found")
            return location
        except (KeyError, TypeError) as e:
            print(f"Default location not found in {self.config_file} file: {e}")
            sys.exit(1)

    @property
    def get_unit(self) -> str:
        """Get default units from config."""
        config = self.config
        try:
            defaults = config.get("defaults", {})
            if not isinstance(defaults, dict):
                raise KeyError("Invalid defaults configuration")
            units = defaults.get("units")
            if not units:
                raise KeyError("Default units not found")
            return units
        except (KeyError, TypeError) as e:
            print(f"Default units not found in {self.config_file} file: {e}")
            sys.exit(1)

    @property
    def city_colour(self) -> str:
        """Get city color from theme."""
        theme = self.theme
        try:
            colours = theme.get("colours", {})
            if not isinstance(colours, dict):
                raise KeyError("Invalid colours configuration")
            return colours.get("col_city", "light_steel_blue")
        except (KeyError, TypeError):
            print(f'No default city colour found in theme. Using default: "light_steel_blue"')
            return "light_steel_blue"

    def temp_colour(self, temperature: float) -> str:
        """Get temperature color based on value."""
        theme = self.theme
        try:
            colours = theme.get("colours", {})
            if not isinstance(colours, dict):
                raise KeyError("Invalid colours configuration")
            temp_colours = colours.get("col_temp", {})
            if not isinstance(temp_colours, dict):
                raise KeyError("Invalid temperature colours configuration")
            
            if temperature > 30:
                return temp_colours.get("high", "sandy_brown")
            elif temperature >= 10:
                return temp_colours.get("mid", "chartreuse3")
            else:
                return temp_colours.get("low", "deep_sky_blue1")
        except (KeyError, TypeError):
            print(f"No temperature colours found in theme. Using default.")
            return "chartreuse3"

    def humid_colour(self, humidity: int) -> str:
        """Get humidity color based on value."""
        theme = self.theme
        try:
            colours = theme.get("colours", {})
            if not isinstance(colours, dict):
                raise KeyError("Invalid colours configuration")
            humid_colours = colours.get("col_humid", {})
            if not isinstance(humid_colours, dict):
                raise KeyError("Invalid humidity colours configuration")
            
            if humidity > 65:
                return humid_colours.get("high", "cornflower_blue")
            elif humidity >= 55:
                return humid_colours.get("mid", "green_yellow")
            else:
                return humid_colours.get("low", "indian_red")
        except (KeyError, TypeError):
            print(f"No humidity colours found in theme. Using default.")
            return "green_yellow"

    def condition_colour(self, condition: str) -> str:
        """Get weather condition color based on condition type."""
        theme = self.theme
        try:
            colours = theme.get("colours", {})
            if not isinstance(colours, dict):
                raise KeyError("Invalid colours configuration")
            desc_colours = colours.get("col_desc", {})
            if not isinstance(desc_colours, dict):
                raise KeyError("Invalid description colours configuration")

            defaults = {
                "Thunderstorm": "dodger_blue2",
                "Drizzle": "deep_sky_blue2",
                "Rain": "light_steel_blue3",
                "Snow": "bright_white",
                "Atmosphere": "grey53",
                "Clear": "dark_orange",
                "Clouds": "orchid"
            }
            
            return desc_colours.get(condition, defaults.get(condition, "dark_orange"))
            
        except (KeyError, TypeError):
            print(f'No condition colours found in theme. Using default.')
            return "dark_orange"

    @property
    def wind_colour(self) -> str:
        """Get wind color from theme."""
        theme = self.theme
        try:
            colours = theme.get("colours", {})
            if not isinstance(colours, dict):
                raise KeyError("Invalid colours configuration")
            return colours.get("col_wind", "sky_blue1")
        except (KeyError, TypeError):
            print(f"No wind colour found in theme. Using default.")
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
          .....:+=...........        
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
        ...        *                        *       *
          ...   *         * ..   ...                        *
 *          ...        *           *            *
              ...               ...                          *
                ..                            *
        *        ..        *                       *
               __##____              *                      *
  *        *  /  ##  ****                   *
             /        ****               *         *  X   *
   *        /        ******     *                    XXX      *
           /___________*****          *             XXXXX
            |            ***               *       XXXXXXX   X
        *   | ___        |                    *   XXXXXXXX  XXX
  *         | | |   ___  | *       *             XXXXXXXXXXXXXXX
            | |_|   | |  ****             *           X   XXXXXXX
        *********** | | *******      *                X      X
****    ********************************************************"""
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
                      ==+         
               ....+========      
             .......=========     
             ...........=====     
          ..............-+===     
         ..................-      
         ...................      
           ................"""
            elif icon == "02n":
                return r"""
                    ###         
               ....#########      
             .......#########     
             ..........:#####     
          ..............+####     
         ..................=      
         ...................      
           ................"""
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
                      ==+         
               ....+========      
             .......=========     
             ...........=====     
          ..............-+===     
         ..................-      
         ...................      
           ................"""

    def get_panel_attribute(self, key):
        return self.theme.get("panel", {}).get(key)

    def get_box_style(self):
        try:
            from rich import box
            box_style = self.theme.get("panel", {}).get("box").upper()
            box_object = getattr(box, box_style)
            return box_object
        except AttributeError as e:
            print(f"Error getting box attribute value from config. [{self.get_theme()}]")
            sys.exit(1)

    def get_ascii_panel_attribute(self,key):
        return self.theme.get("ascii_panel", {}).get(key)

    def get_ascii_box_style(self):
        try:
            from rich import box
            box_style = self.theme.get("ascii_panel", {}).get("box").upper()
            box_object = getattr(box, box_style)
            return box_object
        except AttributeError as e:
            print(f"Error getting box attribute value from {self.theme_file}.")
            sys.exit(1)
