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
