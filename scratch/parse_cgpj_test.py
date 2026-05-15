import os
from bs4 import BeautifulSoup

file_path = r"G:\Mi unidad\Proyectos\IPA27_project\data\raw\cgpj\cgpj_2025_Q4.html"

with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

tables = soup.find_all('table')
print(f"Encontradas {len(tables)} tablas en el documento.")

for i, table in enumerate(tables):
    print(f"\n--- TABLA {i+1} ---")
    headers = [th.text.strip() for th in table.find_all('th')]
    print("Cabeceras:", headers)
    
    rows = table.find_all('tr')
    print(f"Número de filas de datos: {len(rows)}")
    for j, row in enumerate(rows[:5]):
        cols = [td.text.strip() for td in row.find_all('td')]
        if cols:
            print(f"  Fila {j}: {cols}")
