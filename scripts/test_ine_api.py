import requests

print("Provisional - 59238")
url = "https://servicios.ine.es/wstempus/js/ES/TABLAS_OPERACION/59238" # Not sure if it's the right endpoint
url = "https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/59238.csv"
r = requests.get(url, verify=False)
print("status:", r.status_code)
if r.status_code == 200:
    lines = r.text.split('\n')
    for i in range(10): 
        if i < len(lines): print(lines[i][:100])

print("\nDefinitive - 56940")
url = "https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/56940.csv"
r = requests.get(url, verify=False)
print("status:", r.status_code)
if r.status_code == 200:
    lines = r.text.split('\n')
    for i in range(10): 
        if i < len(lines): print(lines[i][:100])
