import pandas as pd
import os

def test_excel_parser(file_path):
    xl = pd.ExcelFile(file_path)
    resultados = []
    
    # Mapeo de nombres de pestañas a codigos de region
    region_map = {
        'Andaluca': 'AND', 'Aragn': 'ARA', 'Asturias': 'AST', 'Baleares': 'BAL',
        'Canarias': 'CAN', 'Cantabria': 'CANT', 'Castilla y Len': 'CYL', 'Castilla - La Mancha': 'CLM',
        'Catalua': 'CAT', 'Valenciana': 'VAL', 'Extremadura': 'EXT', 'Galicia': 'GAL',
        'Madrid': 'MAD', 'Murcia': 'MUR', 'Navarra': 'NAV', 'Pas Vasco': 'PV', 'Rioja': 'RIO',
        'Nacional': 'ESP'
    }
    
    for sheet in xl.sheet_names:
        # Intentar emparejar el nombre de la pestana
        region_code = None
        for key, code in region_map.items():
            if key.lower() in sheet.lower().replace('í','i').replace('á','a').replace('ó','o').replace('ú','u').replace('ñ','n'):
                region_code = code
                break
        
        if not region_code: continue
        
        df = xl.parse(sheet)
        
        # 1. Corrupcion (Buscamos "Total" en la tabla de acusados - suele estar en fila 8)
        # Pero mejor buscar por texto
        try:
            # Buscar fila que contenga "Total" en la primera columna
            mask_total = df.iloc[:, 0].astype(str).str.contains('Total', case=False, na=False)
            filas_total = df[mask_total]
            
            # El primer "Total" (fila 8 aprox) es el de Acusados (Corrupcion)
            cor_val = filas_total.iloc[0, 1] if not filas_total.empty else 0
            
            # El segundo "Total" (fila 36 aprox) es el de Eficiencia
            if len(filas_total) >= 2:
                ing = filas_total.iloc[-1, 1]
                res = filas_total.iloc[-1, 3]
            else:
                ing, res = 0, 0
                
            resultados.append({
                'region': region_code,
                'cor': float(cor_val) if pd.notnull(cor_val) else 0,
                'ing': float(ing) if pd.notnull(ing) else 0,
                'res': float(res) if pd.notnull(res) else 0
            })
        except Exception as e:
            print(f"Error en pestana {sheet}: {e}")

    return resultados

if __name__ == "__main__":
    path = r"G:\Mi unidad\Proyectos\IPA27_project\data\raw\cgpj\cgpj_2025_Q4.xlsx"
    data = test_excel_parser(path)
    for r in data:
        print(r)
