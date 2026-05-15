import os
from bs4 import BeautifulSoup

def inspect_old_format(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    tables = soup.find_all('table')
    print(f"Archivo: {os.path.basename(file_path)} - Tablas: {len(tables)}")
    
    for i, table in enumerate(tables):
        # Buscar el titulo o cabeceras
        headers = [th.text.strip() for th in table.find_all('th')]
        title = "Sin titulo"
        prev = table.find_previous(['h1', 'h2', 'h3', 'p', 'strong'])
        if prev: title = prev.text.strip()
        
        # Si la tabla tiene "Ingresados" o "procedimientos", nos interesa
        text_content = table.text.lower()
        if 'ingresados' in text_content or 'procedimientos' in text_content:
            print(f"\n[TABLA {i}] {title}")
            print(f"Cabeceras: {headers[:8]}")
            # Ver primera fila
            rows = table.find_all('tr')
            for r in rows:
                cols = r.find_all('td')
                if cols:
                    print(f"Muestra: {[c.text.strip() for c in cols[:4]]}")
                    break

if __name__ == "__main__":
    inspect_old_format(r"G:\Mi unidad\Proyectos\IPA27_project\data\raw\cgpj\cgpj_2016_Q1.html")
