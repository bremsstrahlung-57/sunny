import toml
import sys
from pathlib import Path


class ConfigManager:
    def __init__(self) -> None:
        self.config_dir = Path.cwd() / ".config"
        self.config_file = self.config_dir / "config.toml"
        self._config_data = None

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
            return self.config.get("display").get("col_city")
        except (KeyError, TypeError):
            print(
                f'No default city colour added in {self.config_file}. Default colour: "light_steel_blue"'
            )
            return "light_steel_blue"

    def temp_colour(self, temperature: float):
        try:
            if temperature > 30:
                return self.config.get("display").get("col_temp").get("high")
            elif temperature >= 10:
                return self.config.get("display").get("col_temp").get("mid")
            else:
                return self.config.get("display").get("col_temp").get("low")
        except (KeyError, TypeError):
            print(f"No default temp colour added in {self.config_file}.")
            return "chartreuse3"

    def humid_colour(self, humidity: int):
        try:
            if humidity > 65:
                return self.config.get("display").get("col_humid").get("high")
            elif humidity >= 55:
                return self.config.get("display").get("col_humid").get("mid")
            else:
                return self.config.get("display").get("col_humid").get("low")
        except (KeyError, TypeError):
            print(f"No default humidity colour added in {self.config_file}.")
            return "green_yellow"

    def condition_colour(self, condition: str):
        try:
            if condition == "Thunderstorm":
                return self.config.get("display").get("col_desc").get("Thunderstorm")
            elif condition == "Drizzle":
                return self.config.get("display").get("col_desc").get("Drizzle")
            elif condition == "Rain":
                return self.config.get("display").get("col_desc").get("Rain")
            elif condition == "Snow":
                return self.config.get("display").get("col_desc").get("Snow")
            elif condition == "Atmosphere":
                return self.config.get("display").get("col_desc").get("Atmosphere")
            elif condition == "Clear":
                return self.config.get("display").get("col_desc").get("Clear")
            elif condition == "Clouds":
                return self.config.get("display").get("col_desc").get("Clouds")
        except (KeyError, TypeError):
            print(
                f'No default condition colour ("col_desc") added in {self.config_file}.'
            )
            return "dark_orange"

    @property
    def wind_colour(self):
        try:
            return self.config.get("display").get("col_wind")
        except (KeyError, TypeError):
            print(f"No default wind colour added in {self.config_file}.")
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
