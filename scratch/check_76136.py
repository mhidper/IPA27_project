import requests
import json
from datetime import datetime

url = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/76136?date=20240101:"
print(f"Querying table 76136: {url}")

response = requests.get(url)
data = response.json()

print(f"Total series in 76136: {len(data)}")

# Search for National and Andalucía
has_national = False
has_andalucia = False

for serie in data:
    nombre = serie.get('Nombre', '')
    if 'ndice general' in nombre.lower() and 'ndice' in nombre.lower():
        if 'Nacional' in nombre:
            has_national = True
            print(f"Found National: {nombre}")
            last_p = sorted(serie.get('Data', []), key=lambda x: x['Fecha'], reverse=True)[0]
            dt = datetime.fromtimestamp(last_p['Fecha'] / 1000)
            print(f"  Last period: {dt.strftime('%Y-%m')} (Value: {last_p['Valor']})")
        if 'Andaluc' in nombre:
            has_andalucia = True
            print(f"Found Andalucía: {nombre}")
            last_p = sorted(serie.get('Data', []), key=lambda x: x['Fecha'], reverse=True)[0]
            dt = datetime.fromtimestamp(last_p['Fecha'] / 1000)
            print(f"  Last period: {dt.strftime('%Y-%m')} (Value: {last_p['Valor']})")

if not has_national: print("National General Index NOT found in 76136")
if not has_andalucia: print("Andalucía General Index NOT found in 76136")
