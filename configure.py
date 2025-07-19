import toml
import sys
import os
import glob
from pathlib import Path


class ConfigManager:
    def __init__(self) -> None:
        self.config_dir = Path.cwd() / ".config"
        self.config_file = self.config_dir / "config.toml"
        self._config_data = None
        self.theme_dir = Path.cwd() / ".config" / "themes"
        self.theme_file = None
        self._theme_data = None

    @property
    def config(self):
        if self._config_data is None:
            self._load_config()
        return self._config_data

    def _load_config(self):
        if self.config_file.exists():
            with open(self.config_file, "r") as f:
                self._config_data = toml.load(f)
        else:
            print(f"Config file not found: {self.config_file}")
            self._config_data = {}
            sys.exit(1)

    @property
    def config_file_location(self):
        return self.config_file

    def get_theme(self):
        if self._config_data is None:
            self.config
        try:
            defualt_theme = glob.glob(
                os.path.join(
                    self.theme_dir,
                    f"{self._config_data.get("display").get("theme")}.toml",
                )
            )
            self.theme_file = Path(defualt_theme[0])
            return self.theme_file

        except (FileNotFoundError, AttributeError, KeyError) as e:
            print(f"Error: Theme file not found or inaccessible: {e}")
            sys.exit(1)
            return None

    @property
    def theme(self):
        if self._theme_data is None:
            self._load_theme()
        return self._theme_data

    def _load_theme(self):
        self.get_theme()
        if self.theme_file.exists():
            with open(self.theme_file, "r") as f:
                self._theme_data = toml.load(f)
        else:
            print(f"Config file not found: {self.theme_file}")
            self._theme_data = {}
            sys.exit(1)

    @property
    def get_api_key(self):
        try:
            return self.config.get("api").get("key")

        except (KeyError, TypeError):
            print(f"Key not found in {self.config_file} file")
            sys.exit(1)

    @property
    def get_location(self):
        try:
            return self.config.get("defaults").get("location")

        except (KeyError, TypeError):
            print(f"Default location not found in {self.config_file} file")
            sys.exit(1)

    @property
    def get_unit(self):
        try:
            return self.config.get("defaults").get("units")

        except (KeyError, TypeError):
            print(f"Default units not found in {self.config_file} file")
            sys.exit(1)

    @property
    def city_colour(self):
        try:
            return self.theme.get("colours").get("col_city")
        except (KeyError, TypeError):
            print(
                f'No default city colour added in {self.theme_file}. Default colour: "light_steel_blue"'
            )
            return "light_steel_blue"

    def temp_colour(self, temperature: float):
        try:
            if temperature > 30:
                return self.theme.get("colours").get("col_temp").get("high")
            elif temperature >= 10:
                return self.theme.get("colours").get("col_temp").get("mid")
            else:
                return self.theme.get("colours").get("col_temp").get("low")
        except (KeyError, TypeError):
            print(f"No default temp colour added in {self.theme_file}.")
            return "chartreuse3"

    def humid_colour(self, humidity: int):
        try:
            if humidity > 65:
                return self.theme.get("colours").get("col_humid").get("high")
            elif humidity >= 55:
                return self.theme.get("colours").get("col_humid").get("mid")
            else:
                return self.theme.get("colours").get("col_humid").get("low")
        except (KeyError, TypeError):
            print(f"No default humidity colour added in {self.theme_file}.")
            return "green_yellow"

    def condition_colour(self, condition: str):
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
        except (KeyError, TypeError):
            print(
                f'No default condition colour ("col_desc") added in {self.theme_file}.'
            )
            return "dark_orange"

    @property
    def wind_colour(self):
        try:
            return self.theme.get("colours").get("col_wind")
        except (KeyError, TypeError):
            print(f"No default wind colour added in {self.theme_file}.")
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
