import sys
import json
import requests
import poke_validation as pv
from get_module import get_info
import random
from string import Template


name = input("Introduzca el nombre del Pokémon a procesar: ")

name = pv.validate(name)

pok_name = name.capitalize()

url_base = f"https://pokeapi.co/api/v2/pokemon/{name}"

data_base = get_info(url_base)

pok_n = data_base["id"]

#print(pok_n)

stats = data_base["stats"]

indicadores = []
for item in stats:
    indicadores.append(item["base_stat"])

#print(indicadores)

pok_hp, pok_at, pok_de, pok_ate, pok_dee, pok_ve = indicadores

pok_img = data_base['sprites']['front_default']

#print(pok_ve)


# Aquí se determina el parámetro de pokemon predecesor, si existe.

url_previa = f"https://pokeapi.co/api/v2/pokemon-species/{pok_n}"

data_etapa_previa = get_info(url_previa)

#print(data_etapa_previa['evolves_from_species'])

pok_etapa_previa = data_etapa_previa['evolves_from_species']
if pok_etapa_previa is not None:
    pok_etapa_previa = pok_etapa_previa["name"]
else:
    pok_etapa_previa = ""

if pok_etapa_previa != "":
    pok_etapa_previa = f'Etapa Previa: {pok_etapa_previa}'


#print(pok_etapa_previa)




### Aqui se genera lista de tipos de pokemon

tipos_lista = data_base["types"]

tipos = []
for item in tipos_lista:
    tipos.append(item["type"]["name"])

#print(tipos)

### Procesamiento del comentario sobre el pokemon en español

comentarios = data_etapa_previa["flavor_text_entries"]

filtro = [item["flavor_text"].replace("\n"," ") for item in comentarios if item["language"]["name"] == 'es']

pok_comentario = random.choice(filtro)

#print(pok_comentario)

def genera_span(lista):
    diccionario_es = {
      "normal": "Normal", "fire": "Fuego", "flying": "Volador",
      "steel": "Acero", "water": "Agua", "electric": "Eléctrico",
      "grass": "Planta", "ice": "Hielo", "fighting": "Lucha",
      "poison": "Veneno", "ground": "Tierra", "psychic": "Psíquico",
      "bug": "Bicho", "rock": "Roca", "ghost": "Fantasma",
      "dragon": "Dragón", "dark": "Siniestro", "steel": "Acero",
      "fairy": "Hada" }
    
    span_str = ''
    for item in lista:
        item_es = diccionario_es.get(item)
        span_str = span_str + f'<span class="label {item}">{item_es}</span>'
    return span_str

    

print(tipos)

span_tipo = genera_span(tipos)


####
##  Por hacer:
##  1) generar lista super efectivo contra
##  2) generar lista débil contra
##  3) generar lista resistente contra
##  4) generar lista poco eficaz contra
##  5) generar lista inmune contra
##
## Luego, enviar cada una de las listas anteriores a la función "genera_span".
## Asignar el resultado respectivo a la variable correspondiente en el archivo base2.html
## Ejm: Para super efectivo contra, la variable correspondiente es $span_sup_ef



##  Armar y procesar el template

with open('base2.html','r') as infile:
    entrada = infile.read()

document_template = Template(entrada)

document_template_nuevo = document_template.substitute(
    pok_n = pok_n,
    pok_name = pok_name,
    pok_img = pok_img,
    pok_etapa_previa = pok_etapa_previa,
    pok_hp = pok_hp,
    pok_at = pok_at,
    pok_de = pok_de,
    pok_ate = pok_ate,
    pok_dee = pok_dee,
    pok_ve = pok_ve,
    span_tipo = span_tipo,
    pok_comentario = pok_comentario,
    span_sup_ef = "", 
    span_deb_co = "",
    span_res_co = "",
    span_poe_co = "",
    span_inm_co = "",
    span_ine_co = "")

with open('salida.html','w') as outfile:
    outfile.write(document_template_nuevo)

















