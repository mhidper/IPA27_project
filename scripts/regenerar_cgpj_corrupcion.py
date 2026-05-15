import os
import pandas as pd
from bs4 import BeautifulSoup
import glob
import re

MAPEO_CCAA = {
    'Andalucía': 'AND', 'Aragón': 'ARA', 'Asturias': 'AST', 'Illes Balears': 'BAL',
    'Canarias': 'CAN', 'Cantabria': 'CANT', 'Castilla y León': 'CYL', 
    'Castilla-La Mancha': 'CLM', 'Cataluña': 'CAT', 'C.Valenciana': 'VAL',
    'Comunidad Valenciana': 'VAL', 'Extremadura': 'EXT', 'Galicia': 'GAL',
    'Madrid': 'MAD', 'Murcia': 'MUR', 'Navarra': 'NAV', 'País Vasco': 'PV',
    'La Rioja': 'RIO', 'España': 'ESP'
}

def clean_num(text):
    if not text: return 0
    # Quitar puntos de miles y cambiar coma por punto decimal
    text = text.replace('.', '').replace(',', '.').strip()
    try:
        return float(text)
    except:
        return 0

def parse_table_manual(table):
    data = []
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if cols:
            data.append([c.text.strip() for c in cols])
    return data

def parse_cgpj_html(file_path):
    match = re.search(r'cgpj_(\d{4})_Q(\d)', os.path.basename(file_path))
    if not match: return []
    
    anio, trimestre = int(match.group(1)), int(match.group(2))
    periodo, fecha = f"{anio}-Q{trimestre}", f"{anio}-{(trimestre-1)*3 + 1:02d}-01"
    
    print(f"   Procesando {periodo}...")
    
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    tables = soup.find_all('table')
    if len(tables) < 11:
        print(f"      Archivo incompleto (Tablas: {len(tables)})")
        return []
    
    # Tabla 0: Corrupción (CCAA en col 0, Valor en la última columna)
    data_cor = parse_table_manual(tables[0])
    dict_cor = {row[0]: clean_num(row[-1]) for row in data_cor if len(row) > 1}
    
    # Tabla 10: Eficiencia (CCAA en col 0, Ingresados col 1, Resueltos col 3)
    data_eff = parse_table_manual(tables[10])
    
    registros = []
    for row in data_eff:
        if len(row) < 4: continue
        nombre_raw = row[0]
        region = MAPEO_CCAA.get(nombre_raw)
        if not region: continue
        
        ingresados = clean_num(row[1])
        resueltos = clean_num(row[3])
        gob_eff = round(resueltos / ingresados, 4) if ingresados > 0 else 1.0
        
        # Buscar en dict_cor con match parcial
        gob_cor = 0
        for k, v in dict_cor.items():
            if nombre_raw.split()[0].lower() in k.lower():
                gob_cor = v
                break
                
        registros.append({
            'fecha': fecha, 'region': region, 'Periodo': periodo,
            'procedimientos_corrupcion': gob_cor,
            'procedimientos_ingresados': ingresados,
            'procedimientos_resueltos': resueltos,
            'GOB_EFF': gob_eff, 'GOB_COR': gob_cor
        })
    return registros

def ejecutar_reconstruccion():
    input_dir = r"G:\Mi unidad\Proyectos\IPA27_project\data\raw\cgpj"
    output_file = r"G:\Mi unidad\Proyectos\IPA27_project\data\raw\cgpj_corrupcion_procesado.csv"
    html_files = sorted(glob.glob(os.path.join(input_dir, "*.html")))
    
    print(f"Procesando {len(html_files)} archivos...")
    todos_datos = []
    for f in html_files:
        res = parse_cgpj_html(f)
        if res: todos_datos.extend(res)
    
    if todos_datos:
        df = pd.DataFrame(todos_datos).sort_values(['fecha', 'region'])
        df.to_csv(output_file, index=False)
        print(f"\nEXITO: Reconstruidos {len(df)} registros en {output_file}")
    else:
        print("Error: No se extrajeron datos.")

if __name__ == "__main__":
    ejecutar_reconstruccion()
