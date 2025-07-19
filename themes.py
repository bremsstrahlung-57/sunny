from configure import ConfigManager
from rich.console import Console
from rich import print, box
from rich.panel import Panel
from rich.columns import Columns


def show_all_themes():
    theme = ConfigManager()
    console = Console()
    ASCII_WEATHER = r"""
             ========           
           ============         
          ==============        
          ===============       
          ===============       
          ==============        
           ============+        
             ========+"""

    content = Columns(
        [
            Panel(
                f"Clear",
                box=box.MINIMAL,
            ),
            Panel(
                f"Temp: 25 (Feels like: 26) C",
                box=box.MINIMAL,
            ),
            Panel(
                f"Humidity: 65",
                box=box.MINIMAL,
            ),
            Panel(
                f"Wind: 3 m/s",
                box=box.MINIMAL,
            ),
        ]
    )

    PANEL = Panel(
        content,
        title=f"[{theme.city_colour}]{DEFAULT_LOCATION.capitalize()}[/{theme.city_colour}]",
        border_style=f"{theme.get_panel_attribute('border_style')} {theme.city_colour}",
        box=theme.get_box_style(),
        padding=(
            theme.get_panel_attribute("padding_top_right"),
            theme.get_panel_attribute("padding_bottom_left"),
        ),
        width=theme.get_panel_attribute("width"),
        height=theme.get_panel_attribute("height"),
        subtitle=f"Coord: {weather['coord']['lon'], weather['coord']['lat']} Country: {weather['sys']['country']}",
    )
    ASCII_PANEL = Panel(
        ASCII_WEATHER,
        border_style=f"{theme.get_ascii_panel_attribute('border_style')} {theme.city_colour}",
        box=theme.get_ascii_box_style(),
        padding=(
            theme.get_ascii_panel_attribute("padding_top_right"),
            theme.get_ascii_panel_attribute("padding_bottom_left"),
        ),
        width=theme.get_ascii_panel_attribute("width"),
        height=theme.get_ascii_panel_attribute("height"),
    )

    console.print(ASCII_PANEL)
    console.print(PANEL)


def show_all_ascii():
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
