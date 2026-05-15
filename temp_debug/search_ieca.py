import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = "https://www.juntadeandalucia.es/institutodeestadisticaycartografia/intranet/admin/rest/v1.0"

def search_pib_queries():
    # Intentar buscar consultas que contengan "PIB"
    # No conocemos el endpoint exacto de búsqueda, pero a veces es /consultas
    try:
        url = f"{base_url}/consultas?q=PIB"
        print(f"Buscando consultas en: {url}")
        res = requests.get(url, verify=False, timeout=30).json()
        print(f"Encontradas {len(res)} consultas.")
        for item in res[:20]:
            print(f"ID: {item.get('id')}, Titulo: {item.get('title')}")
    except Exception as e:
        print(f"Error en búsqueda: {e}")

if __name__ == "__main__":
    search_pib_queries()
