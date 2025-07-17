import json
from pathlib import Path

CONFIG_DIR = Path.cwd() / ".config"
CONFIG_FILE = CONFIG_DIR / "config.json"


def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return None


def save_config(config_data):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=2)


def get_api_key():
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
        return data["api"]["key"]
    return None


def get_city_name():
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
        return data["defaults"]["location"]
    return None


def get_unit():
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
        return data["defaults"]["units"]
    return None


def config_file_location():
    return CONFIG_FILE


def city_colour():
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
        return data["display"]["col_city"]


def temp_colour(temperature: float):
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
        if temperature > 30:
            return data["display"]["col_temp"]["high"]
        elif temperature >= 10:
            return data["display"]["col_temp"]["mid"]
        else:
            return data["display"]["col_temp"]["low"]
    return data["display"]["col_temp"]["mid"]


def humid_colour(humidity: int):
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
        if humidity > 65:
            return data["display"]["col_humid"]["high"]
        elif humidity >= 55:
            return data["display"]["col_humid"]["mid"]
        else:
            return data["display"]["col_humid"]["low"]


def desc_colour(condition: str):
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
        if condition == "Thunderstorm":
            return data["display"]["col_desc"]["Thunderstorm"]
        elif condition == "Drizzle":
            return data["display"]["col_desc"]["Drizzle"]
        elif condition == "Rain":
            return data["display"]["col_desc"]["Rain"]
        elif condition == "Snow":
            return data["display"]["col_desc"]["Snow"]
        elif condition == "Atmosphere":
            return data["display"]["col_desc"]["Atmosphere"]
        elif condition == "Clear":
            return data["display"]["col_desc"]["Clear"]
        else:
            return data["display"]["col_desc"]["Clouds"]


def emoji(condition: str, icon: str):
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
 *      ...        *           *            *
          ...               ...                          *
            ..                            *
    *        ..        *                       *
           __##____              *                      *
  *    *  /  ##  ****                   *
         /        ****               *         *  X   *
   *    /        ******     *                    XXX      *
       /___________*****          *             XXXXX
        |            ***               *       XXXXXXX   X
    *   | ___        |                    *   XXXXXXXX  XXX
  *     | | |   ___  | *       *             XXXXXXXXXXXXXXX
        | |_|   | |  ****             *           X   XXXXXXX
    *********** | | *******      *                X      X
************************************************************"""
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


def wind_colour():
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
        return data["display"]["col_wind"]
