
import webbrowser
import os
import time
from get_evo import get_evolution
from build_evo_html import build_evo_html
from build_pokemon_html import build_html
from get_base_info import get_base_pokemon
from get_species_info import get_species
from get_types import get_types_info

def show_pics(html, nombre):
    with open(f'{nombre}.html','w') as f:
        f.write(html)
    print('Las fotos se mostrarán en tu Navegador...')
    time.sleep(2)
    webbrowser.open(f'{nombre}.html')
    time.sleep(5)
    os.remove(f'{nombre}.html')
    