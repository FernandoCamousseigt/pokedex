import string
import sys
import json
import requests
import random                   #random para hacer la seleccion aleatoria del comentario
import poke_validation as pv    #se importa como alias para que tome todo. no por from porque esta la lista y el strip que se debe hacer
from get_module import get_info #from porque me interesa el get info
from poke_comentarios import obtener_comentarios
from poke_span import genera_span
from string import Template

name = input ("Introduzca el nombre del Pokémon a buscar: ")

name = pv.validate(name)    #elnombre que regresa de pv.validate regresa bien escrito y se guarda en name

url_base = f'https://pokeapi.co/api/v2/pokemon/{name}'  #se consulta el pokemon por nombre

data_base = get_info(url_base) #get_info es la funcion creada en get_module.

name = name.capitalize()

pok_n = data_base["id"] #pok_n es el numero del pokemon en base_pk.html  y el id es el de la api
#print(pok_n)

stats = data_base ["stats"]

indicadores = []
for item in stats:  #con el for se recorre la lista stats
    indicadores.append(item["base_stat"])  #toma los base_stat. cada elemento lo va guardando en la lista indicadores

print(indicadores)

#ahora se iguala cada variable a un elemento de la lista (que sabemos es fija), separado por comas
pok_hp, pok_at, pok_de, pok_ate, pok_dee, pok_ve = indicadores

""" el camino lento de lo anterior seria:
pok_hp = indicadores[0]
pok_at = indicadores[1]
pok_de = indicadores[2]
pok_ate = indicadores[3]
pok_dee = indicadores[4]
pok_ve = indicadores[5] """


#obtencion de la imagen (url)
pok_img = data_base['sprites']['front_default']
#print(pok_img)

#----ahora para sacar la info del pokemon etapa preevolucion----
#esta api se consulta por id, que ya la habiamos consultado antes como pok_n
url_previa = f"https://pokeapi.co/api/v2/pokemon-species/{pok_n}"

#se invoca la funcion get info para traer la info de la url_previa
data_etapa_previa = get_info(url_previa)

pok_etapa_previa = data_etapa_previa['evolves_from_species']
if pok_etapa_previa is not None:
    pok_etapa_previa = pok_etapa_previa['name'].capitalize()  #.capitalize = Mayusc ini
else:
    pok_etapa_previa = "" #si no, pok etapa previa es vacío
if pok_etapa_previa != "":
    pok_etapa_previa = f"Etapa anterior: {pok_etapa_previa}"
#print(pok_etapa_previa)

# sacar los TIPOS
tipos_lista = data_base["types"]
print(type(tipos_lista))  ########

tipos = []
for item in tipos_lista:
    tipos.append(item["type"]["name"])
print(tipos)

# ahora se Procesa el comentario sobre el pokemon en español
pok_comentario = obtener_comentarios(pok_n)

### Generacion span tipos
span_tipo = f"Tipo <br> {genera_span(tipos)}"

### Generacion fortalezas y debilidades

url_danio = [item["type"]["url"] for item in tipos_lista]   

# obtencion de indicadores de combate

url_danio = []
for item in tipos_lista:
    url_danio.append(item["type"]["url"])
print(url_danio)

if len(url_danio) == 1:
    data_rel1 = get_info(url_danio[0])

else:
    data_rel1 = get_info(url_danio[0])
    data_rel2 = get_info(url_danio[1])


#super eficaz contra
if len(url_danio) == 1:
    supef_contra = data_rel1["damage_relations"]["double_damage_to"]
else:
    supef_contra = data_rel1["damage_relations"]["double_damage_to"] + data_rel2["damage_relations"]["double_damage_to"] 

    print(supef_contra)

supef_co = [item["name"] for item in supef_contra]
supef_co = set(supef_co)
print(supef_co)

#debil contra

if len(url_danio) == 1:
    debil_contra = data_rel1["damage_relations"]["double_damage_to"]
else:
    debil_contra = data_rel1["damage_relations"]["double_damage_to"] + data_rel2["damage_relations"]["double_damage_to"] 

deb_co = [item["name"] for item in debil_contra]
deb_co = set(deb_co)
print(deb_co)


#resistente contra
if len(url_danio) == 1:
    resistente_contra = data_rel1["damage_relations"]["half_damage_from"]
else:
    resistente_contra = data_rel1["damage_relations"]["half_damage_from"] + data_rel2["damage_relations"]["half_damage_from"] 

res_co = [item["name"] for item in resistente_contra]
res_co = set(res_co)
print(res_co)


#poco eficiente contra
if len(url_danio) == 1:
    pocoeficiente_contra = data_rel1["damage_relations"]["half_damage_to"]
else:
    pocoeficiente_contra = data_rel1["damage_relations"]["half_damage_to"] + data_rel2["damage_relations"]["half_damage_to"] 

poef_co = [item["name"] for item in pocoeficiente_contra]
poef_co = set(poef_co)
print(poef_co)

#inmune contra
if len(url_danio) == 1:
    inmune_contra = data_rel1["damage_relations"]["no_damage_from"]
else:
    inmune_contra = data_rel1["damage_relations"]["no_damage_from"] + data_rel2["damage_relations"]["no_damage_from"] 

inm_co = [item["name"] for item in inmune_contra]
inm_co = set(inm_co)
print(inm_co)


#ineficiente contra
if len(url_danio) == 1:
    ineficiente_contra = data_rel1["damage_relations"]["no_damage_to"]
else:
    ineficiente_contra = data_rel1["damage_relations"]["no_damage_to"] + data_rel2["damage_relations"]["no_damage_to"] 

inef_co = [item["name"] for item in ineficiente_contra]
inef_co = set(inef_co)
print(inef_co)


# Obtencion de span de indicadores

span_supef_co = genera_span(supef_co)

span_deb_co = genera_span(deb_co)

span_res_co = genera_span(res_co)

span_poef_co = genera_span(poef_co)

span_inm_co = genera_span(inm_co)

span_inef_co = genera_span(inef_co)



###Generación del html de salida

with open('base.html', 'r', encoding = 'utf-8') as infile:
    entrada = infile.read()

document_template = Template(entrada)

#se definen los valores de las variables que se va a insertar en el template

document_template_nuevo = document_template.safe_substitute( 
    pok_n = pok_n,                                            
    pok_name = name,                                          
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

with open('output.html','w', encoding = 'utf-8') as f:
    f.write(document_template_nuevo)
