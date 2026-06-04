import pandas as pd
import os
import glob
import re

directory = r'G:\Mi unidad\Proyectos\IPA27_project\data\raw\Datos Violencia Mujer CGPJ'
files = glob.glob(os.path.join(directory, '*.xlsx'))

# Mapeo de Comunidades a codigos IPA27
region_map = {
    'andaluc': 'AND',
    'arag': 'ARA',
    'asturias': 'AST',
    'balears': 'BAL',
    'canarias': 'CAN',
    'cantabria': 'CNT',
    'castilla y le': 'CYL',
    'castilla la mancha': 'CLM',
    'catalu': 'CAT',
    'valenciana': 'VAL',
    'extremadura': 'EXT',
    'galicia': 'GAL',
    'madrid': 'MAD',
    'murcia': 'MUR',
    'navarra': 'NAV',
    'vasco': 'PVA',
    'rioja': 'RIO'
}

def parse_filename(filename):
    name = os.path.basename(filename).lower()
    
    year_match = re.search(r'(201\d|202\d)', name)
    year = year_match.group(1) if year_match else None
    
    q = None
    if 'primer' in name or '1 t' in name or '1º' in name:
        q = 'Q1'
    elif 'segundo' in name or '2 t' in name or '2º' in name:
        q = 'Q2'
    elif 'tercer' in name or '3 t' in name or '3º' in name:
        q = 'Q3'
    elif 'cuarto' in name or '4 t' in name or '4º' in name:
        q = 'Q4'
        
    return f"{year}{q}" if year and q else name

def get_region_code(sheet_name):
    s = sheet_name.lower()
    for key, code in region_map.items():
        if key in s:
            return code
    return None

results = []

for f in files:
    period = parse_filename(f)
    print(f"Processing {period}...")
    try:
        xls = pd.ExcelFile(f)
        for sheet in xls.sheet_names:
            region_code = get_region_code(sheet)
            if not region_code:
                continue
                
            df = pd.read_excel(xls, sheet_name=sheet)
            
            denuncias = None
            victimas = None
            victimas_10k = None
            
            for idx, row in df.iterrows():
                val = str(row.iloc[1]).lower()
                
                # Extraccion de metricas - Columna D (Unnamed: 3) es el ao actual
                if 'denuncias recibidas - total' in val:
                    denuncias = row.iloc[3]
                elif val.strip() == 'vctimas' or val.strip() == 'víctimas':
                    victimas = row.iloc[3]
                elif '10.000' in val and 'mujeres' in val:
                    victimas_10k = row.iloc[3]
                    
            results.append({
                'Periodo': period,
                'Region': region_code,
                'Denuncias': denuncias,
                'Victimas': victimas,
                'Victimas_10k': victimas_10k
            })
            
    except Exception as e:
        print(f"Error reading {f}: {e}")

df_final = pd.DataFrame(results)

# Convertir a periodos de tiempo standard de pandas (ej: 2022Q1)
# y luego a datetime para que cruce con el IPA27
df_final['Periodo'] = pd.to_datetime(df_final['Periodo'].str[:4] + '-' + df_final['Periodo'].str[4:].map({'Q1':'01', 'Q2':'04', 'Q3':'07', 'Q4':'10'}) + '-01')
df_final = df_final.sort_values(['Periodo', 'Region']).reset_index(drop=True)

out_dir = r'G:\Mi unidad\Proyectos\IPA27_project\data\processed'
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'cgpj_violencia_mujer.csv')
df_final.to_csv(out_path, index=False)

print(f"\nProceso completado. Datos guardados en {out_path}")
print(df_final.head(10))
