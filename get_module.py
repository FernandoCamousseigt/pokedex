import requests
import json


def get_info(url):
    return json.loads(requests.get(url).text)       #se consulta url con GET,toma el texto y lo transforma en JSON

if __name__ == '__main__':
    url = f'https://pokeapi.co/api/v2/pokemon/charmander'
    print(get_info(url))
