import requests

url = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/79182?date=20240101:"
response = requests.get(url)
data = response.json()

for i, serie in enumerate(data):
    nombre = serie.get('Nombre', '')
    if 'Nacional' in nombre and 'General' in nombre and 'ndice' in nombre:
        print(f"{i}: {nombre}")
