import requests
import json

id = 6

url = f"https://pokeapi.co/api/v2/type/{id}/"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)


data = json.loads(response.text)

damage_relations = data["damage_relations"]

debil_contra = damage_relations["double_damage_from"]

tam_debil_contra = len(debil_contra)

tipos_debil_contra = []

for item in debil_contra:
    tipos_debil_contra.append(item["name"])

print(tipos_debil_contra)


