import os
import toml
from pathlib import Path
from rich import print, box
from rich.panel import Panel
from rich.console import Console
from rich.columns import Columns


def show_all_themes():
    """Shows a preview of all themes"""
    console = Console()
    themes_dir = Path.cwd() / "sunny" / ".config" / "themes"
    theme_files = [f for f in os.listdir(themes_dir) if f.endswith(".toml")]

    for theme_file in theme_files:
        theme_path = os.path.join(themes_dir, theme_file)
        with open(theme_path, "r") as f:
            theme = toml.load(f)
        theme_name = theme_file.split(".")[0].capitalize()
        panel_config = theme.get("panel", {})
        border_style = panel_config.get("border_style", "bold")
        box_attr = getattr(box, panel_config.get("box", "ROUNDED"))
        border_colour = panel_config.get("border_colour", "light_steel_blue")
        padding = (
            int(panel_config.get("padding_top_right", 1)),
            int(panel_config.get("padding_bottom_left", 1)),
            int(panel_config.get("padding_top", 0)),
            int(panel_config.get("padding_right", 0)),
            int(panel_config.get("padding_bottom", 0)),
            int(panel_config.get("padding_left", 0)),
        )
        width = int(panel_config.get("width", 55))
        height = int(panel_config.get("height", 12))
        city_colour = theme.get("colours").get("col_city")
        wind_colour = theme.get("colours").get("col_wind")
        temp_mid = theme.get("colours").get("col_temp").get("mid")
        humd_high = theme.get("colours").get("col_humid").get("high")
        Thunderstorm = theme.get("colours").get("col_desc").get("Thunderstorm")
        content = Columns(
            [
                Panel(
                    f"[{Thunderstorm}]Thunderstorm[/{Thunderstorm}]",
                    box=box.MINIMAL,
                ),
                Panel(
                    f"[{temp_mid}]Temp: 25(26) C[/{temp_mid}]",
                    box=box.MINIMAL,
                ),
                Panel(
                    f"[{humd_high}]Humidity: 65[/{humd_high}]",
                    box=box.MINIMAL,
                ),
                Panel(
                    f"[{wind_colour}]Wind: 3 m/s[/{wind_colour}]",
                    box=box.MINIMAL,
                ),
            ]
        )
        PANEL = Panel(
            content,
            title=f"[{city_colour}]{theme_name}[/{city_colour}]",
            border_style=f"{border_style} {border_colour}",
            box=box_attr,
            padding=(
                padding[0],
                padding[1],
            ),
            width=width,
            height=height,
            subtitle=f"Coord: (75.00, 32.00) Country: IN",
        )
        console.print(PANEL)
        console.print("\n\n")


def show_all_ascii():
    """Shows a preview of all ascii arts of weather conditions"""
    print(
        f"1. Thunderstorm\n{r"""                    
                    #####            
               ....=########         
             .......:########        
            ............-######      
          ...............*######     
         ...................*##      
          .....:+=...........        
           ...:==+-........          
               ==                    
              =="""}",
    )
    print(
        f"\n2. Drizzle\n{r"""       
                  #####           
             ......*######        
             .........+#####      
          .............:*###      
          ...............         
            ...#........          
              #### #              
                # ##"""}",
    )
    print(
        f"\n3. Rain\n{r"""
                 . =======        
              .....:+======       
             ..........+===       
           .............:++       
           ...............        
            ...++........         
               # ## #             
                ## #"""}",
    )
    print(
        f"\n4. Snow\n{r"""
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
****    ********************************************************"""}",
    )
    print(
        f"\n5. Atmosphere\n{r"""
               ######             
            ##########            
               #############      
          #############           
             #############        
               ########"""}",
    )
    print(
        f"\n6. Clear Day\n{r"""
               ========           
             ============         
            ==============        
            ===============       
            ===============       
            ==============        
             ============+        
               ========+"""}",
    )
    print(
        f"\n7. Clear Night\n{r"""         
               ########           
             ############         
            ##############        
            ###############       
            ###############       
            ##############        
             #############        
               #########"""}",
    )
    print(
        f"\n8. Few Clouds Day\n{r"""                             
                      ==+         
               ....+========      
             .......=========     
             ...........=====     
          ..............-+===     
         ..................-      
         ...................      
           ................"""}",
    )
    print(
        f"\n9. Few Clouds Night\n{r"""
                    ###         
               ....#########      
             .......#########     
             ..........:#####     
          ..............+####     
         ..................=      
         ...................      
           ................"""}",
    )
    print(
        f"\n10. Scattered Clouds\n{r"""
               .....              
              ........            
            .............         
          ..................      
          ..................      
           ................."""}",
    )
    print(
        f"\n11. Overcast Clouds\n{r"""
                    ##            
               .. ######          
             ......+#######       
            ..........:######     
         ..............-######    
         .................*##     
         ..................       
          ................"""}",
    )
