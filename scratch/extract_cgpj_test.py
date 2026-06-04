import pandas as pd
import os
import glob
import re

directory = r'G:\Mi unidad\Proyectos\IPA27_project\data\raw\Datos Violencia Mujer CGPJ'
files = glob.glob(os.path.join(directory, '*.xlsx'))

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

results = []
for f in files:
    period = parse_filename(f)
    try:
        xls = pd.ExcelFile(f)
        # Try to find a sheet containing 'madrid'
        target_sheet = next((s for s in xls.sheet_names if 'madrid' in s.lower()), None)
        if target_sheet:
            df = pd.read_excel(xls, sheet_name=target_sheet)
            # Find row where Unnamed: 1 contains "10.000"
            for idx, row in df.iterrows():
                val = str(row.iloc[1]).lower()
                if '10.000' in val and 'mujeres' in val:
                    # Current year is usually in index 3
                    val_y0 = row.iloc[2]
                    val_y1 = row.iloc[3]
                    
                    # Try to dynamically find the correct column based on the header row (usually 2 or 3 rows above)
                    col_idx = 3
                    for header_idx in range(max(0, idx-15), idx):
                        row_h = df.iloc[header_idx]
                        if isinstance(row_h.iloc[3], str) and str(year) in row_h.iloc[3]:
                            col_idx = 3
                            break
                        elif isinstance(row_h.iloc[2], str) and str(year) in row_h.iloc[2]:
                            col_idx = 2
                            break
                            
                    results.append((period, row.iloc[col_idx], row.iloc[3]))
                    break
    except Exception as e:
        print(f"Error reading {f}: {e}")

# Sort by period
results.sort(key=lambda x: x[0])
for r in results:
    print(r)
