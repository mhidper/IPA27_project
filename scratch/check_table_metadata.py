import requests

url = "https://servicios.ine.es/wstempus/js/ES/METADATOS_TABLA/50913"
response = requests.get(url)
print(response.status_code)
print(response.text[:500])
