import pandas as pd
import os
import glob
from bs4 import BeautifulSoup
import re

def parse_html_cgpj(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    match = re.search(r'cgpj_(\d{4})_Q(\d)', os.path.basename(file_path))
    if not match: return []
    anio, trim = match.groups()
    fecha_base = f"{anio}-{int(trim)*3-2:02d}-01"
    periodo = f"{anio}-Q{trim}"
    
    tables = soup.find_all('table')
    if not tables: return []
    
    region_map = {
        'Andalucía': 'AND', 'Aragón': 'ARA', 'Asturias': 'AST', 'Illes Balears': 'BAL',
        'Canarias': 'CAN', 'Cantabria': 'CANT', 'Castilla y León': 'CYL', 'Castilla-La Mancha': 'CLM',
        'Cataluña': 'CAT', 'C.Valenciana': 'VAL', 'Extremadura': 'EXT', 'Galicia': 'GAL',
        'Madrid': 'MAD', 'Murcia': 'MUR', 'Navarra': 'NAV', 'País Vasco': 'PV', 'La Rioja': 'RIO',
        'España': 'ESP'
    }

    # 1. Acusados
    acusados_data = {}
    rows = tables[0].find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 2:
            region_raw = cols[0].text.strip()
            region_code = next((code for key, code in region_map.items() if key[:5].lower() in region_raw.lower()), None)
            if region_code:
                try:
                    val = float(cols[-1].text.strip().replace('.', '').replace(',', '.'))
                    acusados_data[region_code] = val
                except: continue

    # 2. GOB_COR
    gob_cor_data = {}
    target_table_cor = next((t for t in tables if 'apertura de juicio oral' in t.text.lower()), None)
    if target_table_cor:
        for row in target_table_cor.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) >= 2:
                region_raw = cols[0].text.strip()
                region_code = next((code for key, code in region_map.items() if key[:5].lower() in region_raw.lower()), None)
                if region_code:
                    try:
                        val = float(cols[-1].text.strip().replace('.', '').replace(',', '.'))
                        gob_cor_data[region_code] = val
                    except: continue

    # 3. Eficiencia
    eficiencia_data = {}
    target_table_eff = next((t for t in tables if 'ingresados' in t.text.lower() and 'resueltos' in t.text.lower()), None)
    if target_table_eff:
        for row in target_table_eff.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) >= 4:
                region_raw = cols[0].text.strip()
                region_code = next((code for key, code in region_map.items() if key[:5].lower() in region_raw.lower()), None)
                if region_code:
                    try:
                        ing = float(cols[1].text.strip().replace('.', '').replace(',', '.'))
                        res = float(cols[3].text.strip().replace('.', '').replace(',', '.'))
                        if ing > 0 or res > 0: eficiencia_data[region_code] = (ing, res)
                    except: continue

    return [{'fecha': fecha_base, 'region': reg, 'Periodo': periodo, 
             'procedimientos_corrupcion': acusados_data.get(reg, 0), 
             'procedimientos_ingresados': eficiencia_data.get(reg, (0, 0))[0], 
             'procedimientos_resueltos': eficiencia_data.get(reg, (0, 0))[1],
             'GOB_COR': gob_cor_data.get(reg, 0)} 
            for reg in acusados_data.keys()]

def parse_excel_cgpj(file_path):
    xl = pd.ExcelFile(file_path)
    match = re.search(r'cgpj_(\d{4})_Q(\d)', os.path.basename(file_path))
    if not match: return []
    anio, trim = match.groups()
    fecha_base = f"{anio}-{int(trim)*3-2:02d}-01"
    periodo = f"{anio}-Q{trim}"
    
    region_map = {
        'andal': 'AND', 'arago': 'ARA', 'astur': 'AST', 'balear': 'BAL', 'canari': 'CAN', 'cantab': 'CANT',
        'leon': 'CYL', 'mancha': 'CLM', 'catalu': 'CAT', 'valenc': 'VAL', 'extrem': 'EXT', 'galici': 'GAL',
        'madrid': 'MAD', 'murcia': 'MUR', 'navarr': 'NAV', 'vasco': 'PV', 'rioja': 'RIO', 'centrales': 'ESP_PART'
    }
    
    resultados = []
    for sheet in xl.sheet_names:
        sheet_clean = sheet.lower().replace('í','i').replace('á','a').replace('ó','o').replace('ú','u').replace('ñ','n')
        region_code = next((code for key, code in region_map.items() if key in sheet_clean), None)
        if not region_code: continue
        
        df = xl.parse(sheet)
        try:
            mask_total = df.iloc[:, 0].astype(str).str.contains('Total', case=False, na=False)
            filas_total = df[mask_total]
            cor_acusados = float(filas_total.iloc[0, 1]) if not filas_total.empty else 0
            
            # GOB_COR
            gob_cor = 0
            if region_code == 'ESP_PART':
                # ESPAÑA: El dato real (el 2) esta en las filas 60-70 (Sumarios/Abreviados)
                for i, row in df.iloc[60:70].iterrows():
                    label = str(row.iloc[0]).lower()
                    if any(x in label for x in ['abreviados', 'sumarios', 'jurado']):
                        val = row.iloc[1]
                        try: gob_cor += float(val) if pd.notnull(val) else 0
                        except: pass
            else:
                # CCAA: Sumar bloque Apertura al final
                mask_ap = df.iloc[:, 0:2].apply(lambda r: r.astype(str).str.contains('auto de apertura de juicio oral', case=False).any(), axis=1)
                idxs_ap = df[mask_ap].index
                if not idxs_ap.empty:
                    idx_ap = idxs_ap[-1]
                    for offset in range(1, 10):
                        if idx_ap + offset >= len(df): break
                        label = str(df.iloc[idx_ap + offset, 0]).lower()
                        if any(x in label for x in ['abreviados', 'sumarios', 'jurado']):
                            val = df.iloc[idx_ap + offset, 1]
                            try: gob_cor += float(val) if pd.notnull(val) else 0
                            except: pass
                        if 'total' in label or 'recursos' in label: break

            ing = float(filas_total.iloc[-1, 1]) if len(filas_total) >= 2 else 0
            res = float(filas_total.iloc[-1, 3]) if len(filas_total) >= 2 else 0
            
            resultados.append({
                'fecha': fecha_base, 'region': region_code, 'Periodo': periodo,
                'procedimientos_corrupcion': cor_acusados, 
                'procedimientos_ingresados': ing, 
                'procedimientos_resueltos': res,
                'GOB_COR': gob_cor
            })
        except: continue
        
    # Calcular Total Nacional (ESP)
    esp_data = {
        'fecha': fecha_base, 'region': 'ESP', 'Periodo': periodo,
        'procedimientos_corrupcion': sum(r['procedimientos_corrupcion'] for r in resultados),
        'procedimientos_ingresados': sum(r['procedimientos_ingresados'] for r in resultados),
        'procedimientos_resueltos': sum(r['procedimientos_resueltos'] for r in resultados),
        'GOB_COR': sum(r['GOB_COR'] for r in resultados)
    }
    resultados = [r for r in resultados if r['region'] != 'ESP_PART']
    resultados.append(esp_data)
    return resultados

def main():
    f_copia = r"G:\Mi unidad\Proyectos\IPA27_project\data\raw\cgpj_corrupcion_procesado - copia.csv"
    f_salida = r"G:\Mi unidad\Proyectos\IPA27_project\data\raw\cgpj_corrupcion_procesado.csv"
    raw_dir = r"G:\Mi unidad\Proyectos\IPA27_project\data\raw\cgpj"
    
    if os.path.exists(f_copia):
        df_final = pd.read_csv(f_copia)
        print(f"Cargadas {len(df_final)} filas del historico.")
    else:
        df_final = pd.DataFrame(columns=['fecha', 'region', 'Periodo', 'procedimientos_corrupcion', 'procedimientos_ingresados', 'procedimientos_resueltos', 'GOB_EFF', 'GOB_COR'])

    files = glob.glob(os.path.join(raw_dir, "*.html")) + glob.glob(os.path.join(raw_dir, "*.xlsx"))
    all_new_data = []
    for f in files:
        if f.endswith(".html"): all_new_data.extend(parse_html_cgpj(f))
        else: all_new_data.extend(parse_excel_cgpj(f))
    
    df_new = pd.DataFrame(all_new_data)
    df_final['fecha'] = pd.to_datetime(df_final['fecha']).dt.strftime('%Y-%m-%d')
    
    if not df_new.empty:
        df_new['fecha'] = pd.to_datetime(df_new['fecha']).dt.strftime('%Y-%m-%d')
        fechas_existentes = set(df_final['fecha'].unique())
        df_solo_nuevos = df_new[~df_new['fecha'].isin(fechas_existentes)]
        if not df_solo_nuevos.empty:
            df_final = pd.concat([df_final, df_solo_nuevos], ignore_index=True)
            print(f"Anadidos {len(df_solo_nuevos)} registros nuevos.")
    
    if 'GOB_EFF' not in df_final.columns: df_final['GOB_EFF'] = 1.0
    if 'fechas_existentes' in locals():
        mask_new = ~df_final['fecha'].isin(fechas_existentes)
        df_final.loc[mask_new, 'GOB_EFF'] = df_final[mask_new].apply(lambda r: r['procedimientos_resueltos'] / r['procedimientos_ingresados'] if r['procedimientos_ingresados'] > 0 else 1.0, axis=1)
    
    df_final.sort_values(['fecha', 'region']).to_csv(f_salida, index=False)
    print(f"Archivo generado con exito: {f_salida} ({len(df_final)} registros)")

if __name__ == "__main__":
    main()
