#modulo comentario sobre descripcion de pokemon

import random                       #random para hacer la seleccion aleatoria del comentario
from get_module import get_info     #from porque me interesa el get info

def obtener_comentarios(pok_n):

    url_previa = f"https://pokeapi.co/api/v2/pokemon-species/{pok_n}"

    #se invoca al funcion get info para traer la info de la url_previa
    data_etapa_previa = get_info(url_previa)

    comentarios = data_etapa_previa["flavor_text_entries"]   #Procesa el comentario sobre el pokemon en español

    filtro = []
    for item in comentarios:
        if item["language"]["name"] == 'es':
            filtro.append(item["flavor_text"].replace("\n"," "))  #("\n"," ")se sustiyue el salto de linea por espacio en blanco

#El filtro también se podría hacer con comprehension:
#para un diccionario es filtro = {k:v for k,v in diccionario.items() if v>umbral}
#pero flavor text entries tenemos una lista de diccionarios. hay que adaptarlo:
#esta es la version comprehension:
#filtro = [item["flavor_text"].replace("\n"," ") for item in comentarios if item["language"]["name"] == 'es']

    pok_comentario = random.choice(filtro)    #para tomar un comentario al azar se utiliza random choice
    print(pok_comentario)

    return pok_comentario