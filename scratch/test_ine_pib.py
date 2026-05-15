import requests

url = "https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/CNTR6652?nult=5"
response = requests.get(url)
data = response.json()

print(f"Series: {data.get('Nombre')}")
for p in data.get('Data', []):
    print(f"  Year: {p['Anyo']}, Period: {p['FK_Periodo']}, Value: {p['Valor']}")
