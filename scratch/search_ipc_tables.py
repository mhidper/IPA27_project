import requests

base_url = "https://servicios.ine.es/wstempus/js/ES"
url = f"{base_url}/OPERACIONES_DISPONIBLES"
response = requests.get(url).json()

for op in response:
    if "IPC" in op['Nombre'].upper():
        url_tablas = f"{base_url}/TABLAS_OPERACION/{op['Id']}"
        tablas = requests.get(url_tablas).json()
        for t in tablas:
            if "nacional" in t['Nombre'].lower() and "general" in t['Nombre'].lower():
                print(f"Table: {t['Id']} - {t['Nombre']}")
