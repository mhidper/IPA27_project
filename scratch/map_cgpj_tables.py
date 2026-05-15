import os
from bs4 import BeautifulSoup
import pandas as pd

def map_cgpj_tables(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    tables = soup.find_all('table')
    print(f"Analizando {file_path}...")
    
    for i, table in enumerate(tables):
        # Intentar encontrar el título arriba de la tabla
        title = "Sin título"
        prev = table.find_previous(['h1', 'h2', 'h3', 'p', 'strong'])
        if prev:
            title = prev.text.strip()
        
        headers = [th.text.strip() for th in table.find_all('th')]
        print(f"\n[TABLA {i}] {title}")
        print(f"Cabeceras: {headers[:5]}...") # Mostrar solo las primeras
        
        # Mostrar la primera fila de datos para verificar
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if cols:
                print(f"Muestra: {[c.text.strip() for c in cols[:3]]}")
                break

if __name__ == "__main__":
    path = r"G:\Mi unidad\Proyectos\IPA27_project\data\raw\cgpj\cgpj_2024_Q4.html"
    map_cgpj_tables(path)
