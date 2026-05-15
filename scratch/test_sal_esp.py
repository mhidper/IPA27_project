import requests

def test_id(tabla_id):
    url = f"https://servicios.ine.es/wps/utils/serviciosRest/JSON/es/DATOS_TABLA/{tabla_id}?nult=1"
    print(f"Probando Tabla {tabla_id}...")
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data:
                print(f"EXITO: {data[0]['Nombre']}")
                print(f"Ultimo dato: {data[0]['Data'][0]['Anyo']} -> {data[0]['Data'][0]['Valor']}")
            else:
                print("Vacia")
        else:
            print(f"Error {r.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_id("13880")
    test_id("1448")
    test_id("1414")
