from queue import Empty
import sys
import json
import requests
import random
import poke_validation as pv
from get_module import get_info
from string import Template

name = input ("Introduzca el nombre del Pokemon a buscar :")

name = pv.validate(name)

url_base = f'https://pokeapi.co/api/v2/pokemon/{name}'

data_base = get_info(url_base) #get_info es la funcion creada en get_module.

name = name.capitalize()

pok_n = data_base["id"]
#print(pok_n)

stats = data_base ["stats"]
print(stats)

indicadores = []
for item in stats:
    indicadores.append(item["base_stat"])

print(indicadores)

#ahora se iguala cada variable a un elemento de la lista (que sabemos es fija), separado por comas
pok_hp, pok_at, pok_de, pok_ate, pok_dee, pok_ve = indicadores

#print(pok_hp)


#--- ahora para sacar la imagen (la url)----
pok_img = data_base['sprites']['front_default']
#print(pok_img)

#----ahora para sacar la info del pokemon etapa preevolucion----
#esta api se consulta por id, que ya la habiamos consultado antes como pok_n
url_previa = f"https://pokeapi.co/api/v2/pokemon-species/{pok_n}"

#se invoca al funcion get info para traer la info de la url_previa
data_etapa_previa = get_info(url_previa)


pok_etapa_previa = data_etapa_previa['evolves_from_species']

if pok_etapa_previa is not None:
    pok_etapa_previa = pok_etapa_previa['name']

else:
    pok_etapa_previa = "" #si no, pok etapa previa es vacío

if pok_etapa_previa != "":
    pok_etapa_previa = f"Etapa anterior: {pok_etapa_previa}"



#print(pok_etapa_previa)

# sacar los TIPOS

tipos_lista = data_base["types"]
print(type(tipos_lista))

tipos = []
for item in tipos_lista:
    tipos.append(item["type"]["name"])
print(tipos)



"""esta es la version comprehension:
filtro = [item["flavor_text"].replace("\n"," ") for item in comentarios if item["language"]["name"] == 'es']"""

# ahora se Procesa el comentario sobre el pokemon en español

comentarios = data_etapa_previa["flavor_text_entries"]
#print(comentarios)


filtro = []
for item in comentarios:
    if item["language"]["name"] == 'es':
        filtro.append(item["flavor_text"].replace("\n"," "))

#("\n"," ")se sustiyue el salto de linea por espacio en blanco

#print(filtro)

pok_comentario = random.choice(filtro)
print(pok_comentario)

### Generacion span tipos

def genera_span(lista):
    diccionario_es = {
      "normal": "Normal", "fire": "Fuego", "flying": "Volador",
      "steel": "Acero", "water": "Agua", "electric": "Eléctrico",
      "grass": "Planta", "ice": "Hielo", "fighting": "Lucha",
      "poison": "Veneno", "ground": "Tierra", "psychic": "Psíquico",
      "bug": "Bicho", "rock": "Roca", "ghost": "Fantasma",
      "dragon": "Dragón", "dark": "Siniestro", "steel": "Acero",
      "fairy": "Hada" }
    
    span_str= ""
    for item in lista:
        item_es = diccionario_es.get(item)
        span_str = span_str + f'<span class="label {item}">{item_es}</span>'
    return span_str

#print(tipos)

span_tipo = genera_span(tipos)

#print(span_tipo)

### Generacion fortalezas y debilidades

#Se busca el numero del tipo de pokemon e inyectarlo en la url#
url_danio = []
for item in tipos_lista:
    url_danio.append(item["type"]["url"])
print(url_danio)

#se invoca al funcion get info para traer la info de la url_danio
data_rel_danio = get_info(url_danio[0])


#super eficaz contra
supef_contra = data_rel_danio["damage_relations"]["double_damage_to"]

supef_co =[]
for item in supef_contra:
    supef_co.append(item["name"])

print(f"supereficaz = {supef_co}")

#debil contra
deb_co = [deb_co["name"] for deb_co in data_rel_danio["damage_relations"]["double_damage_from"]]
print(deb_co)

#resistente contra
res_co = [res_co["name"] for res_co in data_rel_danio["damage_relations"]["half_damage_from"]] 
print(res_co)

#poco eficiente
poef_co = [poef_co["name"] for poef_co in data_rel_danio["damage_relations"]["half_damage_to"]] 
print(poef_co)

#inmune contra
inm_co = [inm_co["name"] for inm_co in data_rel_danio["damage_relations"]["no_damage_from"]] 
print(inm_co)

#ineficiente contra
inef_co = [inef_co["name"] for inef_co in data_rel_danio["damage_relations"]["no_damage_to"]] 
print(inef_co)


if len(supef_co) > 0:
    span_supef_co = genera_span(supef_co)
    span_supef_co = f"Super Efectivo contra: <br> {span_supef_co}"
else:
    span_supef_co = ""


if len(deb_co) > 0:
    span_deb_co = genera_span(deb_co)
    span_deb_co = f"Debil contra: <br> {span_deb_co}"
else:
    span_deb_co = ""


if len(res_co) > 0:
    span_res_co = genera_span(res_co)
    span_res_co = f"Resistente contra: <br> {span_res_co}"
else:
    span_res_co = ""


if len(poef_co) > 0:
    span_poef_co = genera_span(poef_co)
    span_poef_co = f"Resistente contra: <br> {span_poef_co}"
else:
    span_poef_co = ""


if len(inm_co) > 0:
    span_inm_co = genera_span(inm_co)
    span_inm_co = f"Inmune contra: <br> {span_inm_co}"
else:
    span_inm_co = ""


if len(inef_co) > 0:
    span_inef_co = genera_span(inef_co)
    span_inef_co = f"Ineficiente contra: <br> {span_inef_co}"
else:
    span_inef_co = ""



###Generación del html de salida

with open('base_pk_3.html', 'r') as infile:
    entrada = infile.read()

document_template = Template(entrada)

#se definen los valores de las variables que se va a insertar en el template

document_template_nuevo = document_template.safe_substitute(  #document_template_nuevo recibe lo que se va a sustituir
    pok_n = pok_n,                                            #debe respetarse el orden nombre_var_html = nombre_var_python
    pok_name = name,                                          #como hay más de 1 variable, se separan por coma
    pok_etapa_previa = pok_etapa_previa,
    pok_hp = pok_hp,
    pok_at = pok_at,
    pok_de = pok_de, 
    pok_ate = pok_ate, 
    pok_dee = pok_dee, 
    pok_ve = pok_ve,
    pok_img = pok_img,
    span_tipo = span_tipo,
    pok_comentario = pok_comentario,
    span_supef_co = span_supef_co,
    span_deb_co = span_deb_co,
    span_res_co = span_res_co,
    span_poef_co = span_poef_co,
    span_inm_co = span_inm_co,
    span_inef_co = span_inef_co)


with open('salida_pk_3.html','w') as f:
    f.write(document_template_nuevo)
