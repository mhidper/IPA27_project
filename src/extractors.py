import pandas as pd
import requests
import os
import io
import re
from .config import DATA_RAW, DATA_PROCESSED
from .connectors import IneConnector

ine = IneConnector()

def extract_ipc():
    """Extracts Monthly General CPI for Spain and Andalucía."""
    return ine.download_tempus("50913", "IPC_General")

def extract_societies():
    """Extracts Monthly Company Creation figures."""
    return ine.download_tempus("13912", "Creacion_Empresas")

def extract_pib():
    """Extracts Quarterly GDP combining IECA (Andalucía) and INE (Spain)."""
    # Spain from INE (Series CNTR6652)
    url_esp = "https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/CNTR6652?nult=500"
    print("⬇️ Downloading Quarterly GDP Spain (INE)...")
    try:
        r = requests.get(url_esp, timeout=30, verify=False)
        data_esp = r.json()
        regs_esp = []
        for item in data_esp['Data']:
            fecha = pd.to_datetime(item['Fecha'], unit='ms')
            regs_esp.append({
                'Fecha': fecha,
                'Periodo': f"{fecha.year}-Q{(fecha.month-1)//3 + 1}",
                'Region': 'ESP',
                'Indicador': 'PIB_Trimestral',
                'Valor': item['Valor'],
                'Frecuencia': 'Trimestral',
                'Serie_Original': 'INE_PIB_Ajustado_Indice_Volumen'
            })
        df_esp = pd.DataFrame(regs_esp)
    except Exception as e:
        print(f"❌ Error downloading GDP Spain: {e}")
        df_esp = pd.DataFrame()

    # Andalucía from IECA
    url_and = "https://www.juntadeandalucia.es/institutodeestadisticaycartografia/intranet/admin/rest/v1.0/consulta/27669?D_CRTA_COMPONPIB2008_0=69634&D_TEMPORAL_0=1809,1813,1818,1822,1828,1832,1837,1841,1847,1851,1856,1860,1866,1870,1875,1879,1885,1889,1894,1898,1904,1908,1913,1917,1923,1927,1932,1936,1942,1946,1951,1955,1961,1965,1970,1974,1980,1984,1989,1993,1999,2003,2008,2012,2018,2022,2027,2031,2037,2041,2046,2050,2056,2060,2065,2069,2075,2079,2084,2088,2094,2098,2103,2107,2113,2117,2122,2126,2132,2136,2141,2145,2151,2155,2160,2164,2170,2174,2179,2183,2189,2193,2198,2202,2224,2228,2233,2237,55483,55487,55492,55496,55502,55506,55511,55515,55521,55525,55530,55534,180141,180145,180150,180154,180160,180164,180169,180173,180179,180183,180188,180192,180198,180202,180207,180211,180217,180221"
    print("Downloading Quarterly GDP Andalucía (IECA)...")
    try:
        r = requests.get(url_and, timeout=30, verify=False)
        data_and = r.json()
        regs_and = []
        for item in data_and['data']:
            periodo_raw = item[1]['cod'][0]
            anio = int(periodo_raw[:4])
            trimestre = int(periodo_raw[4])
            mes_inicio = (trimestre - 1) * 3 + 1
            regs_and.append({
                'Fecha': pd.to_datetime(f"{anio}-{mes_inicio:02d}-01"),
                'Periodo': f"{anio}-Q{trimestre}",
                'Region': 'AND',
                'Indicador': 'PIB_Trimestral',
                'Valor': float(item[4]['val']),
                'Frecuencia': 'Trimestral',
                'Serie_Original': 'IECA_PIB_Indice_Volumen'
            })
        df_and = pd.DataFrame(regs_and)
    except Exception as e:
        print(f"❌ Error downloading GDP Andalucía: {e}")
        df_and = pd.DataFrame()

    df = pd.concat([df_and, df_esp], ignore_index=True).sort_values(['Region', 'Fecha'])
    path = os.path.join(DATA_PROCESSED, "PIB_Trimestral.csv")
    df.to_csv(path, index=False)
    print(f"   ✅ Saved: PIB_Trimestral.csv ({len(df)} records)")
    return df

def extract_life_expectancy():
    """Extracts Life Expectancy data using multi-table JAXI logic."""
    return ine.download_jaxi_long(
        table_ids={'ESP': '27153', 'AND': '27154'},
        name="Esperanza_Vida",
        filters={
            "Funciones": "Esperanza de vida",
            "Edad": "0 a",
            "Sexo": "Ambos"
        }
    )

def extract_abandono_escolar():
    """Extracts School Dropout Rate."""
    return ine.download_jaxi_long(
        table_ids="69786",
        name="Abandono_Escolar"
    )

def extract_id_expenditure():
    """Extracts R&D Expenditure as % of GDP."""
    return ine.download_jaxi_long(
        table_ids={'ESP': '76751', 'AND': '76795'},
        name="Gasto_ID_PIB"
    )

def extract_tech_employment():
    """Extracts Employment in Tech sectors from Social Security data."""
    path = os.path.join(DATA_RAW, "Afiliados_SS.csv")
    if not os.path.exists(path):
        print(f"⚠️ {path} not found. Please move the Social Security CSV (Afiliados medios) to this location.")
        return None
    
    df = pd.read_csv(path, encoding='ISO-8859-15', skiprows=1, sep=';')
    # Use logic from main.ipynb
    df.columns = ['Periodo', 'Total_ESP', 'Total_AND', 'J_ESP', 'J_AND', 'M_ESP', 'M_AND', 'S_ESP', 'S_AND']
    df['Fecha'] = pd.to_datetime(df['Periodo'].astype(str), format='%Y%m')
    
    # Calculate % knowledge-intensive (J+M+S proxy or as defined in main.ipynb)
    # Replicating main.ipynb: Pct_Conocimiento = ((J + M + S) / Total) * 100
    df['Pct_Conocimiento_ESP'] = ((df['J_ESP'] + df['M_ESP'] + df['S_ESP']) / df['Total_ESP']) * 100
    df['Pct_Conocimiento_AND'] = ((df['J_AND'] + df['M_AND'] + df['S_AND']) / df['Total_AND']) * 100
    
    # Transform to long format
    records = []
    for _, row in df.iterrows():
        for reg in ['ESP', 'AND']:
            records.append({
                'Fecha': row['Fecha'],
                'Periodo': f"{row['Fecha'].year}-M{row['Fecha'].month:02d}",
                'Region': reg,
                'Indicador': 'Ocupados_Tech',
                'Valor': row[f'Pct_Conocimiento_{reg}'],
                'Frecuencia': 'Mensual',
                'Serie_Original': 'SS_Afiliados_JMS'
            })
    
    df_res = pd.DataFrame(records)
    df_res.to_csv(os.path.join(DATA_PROCESSED, "Ocupados_Tech.csv"), index=False)
    return df_res

def extract_ict_access():
    """Processes ICT microdata for 2016-2025 (Fixed-width and TAB formats)."""
    base_path = os.path.join(DATA_RAW, "acceso TIC")
    if not os.path.exists(base_path):
        print(f"⚠️ Microdata path {base_path} not found.")
        return None
        
    archivos = {
        2016: ("Fichero Cuestionario 2016.txt", 1, 2, 150, 1, 49, 13),
        2017: ("Fichero Cuestionario 2017.txt", 1, 2, 151, 1, 49, 13),
        2018: ("Fichero Cuestionario 2018.txt", 1, 2, 154, 1, 52, 13),
    }
    
    resultados = []
    
    # Process Fixed Width (2016-2018)
    for anio, (fname, p_ccaa, t_ccaa, p_viv, t_viv, p_fac, t_fac) in archivos.items():
        path = os.path.join(base_path, fname)
        if os.path.exists(path):
            with open(path, 'r', encoding='latin-1') as f:
                lines = f.readlines()
            regs = []
            for line in lines:
                ccaa = line[p_ccaa-1:p_ccaa-1+t_ccaa].strip()
                viv = line[p_viv-1:p_viv-1+t_viv].strip()
                fac = line[p_fac-1:p_fac-1+t_fac].strip().replace(',', '.')
                try: regs.append({'CCAA': ccaa, 'VIV_INTER': viv, 'FACTOR_H': float(fac)})
                except: continue
            
            df_y = pd.DataFrame(regs)
            df_valid = df_y[df_y['VIV_INTER'].isin(['1', '6'])].copy()
            df_valid['TIENE_INTERNET'] = (df_valid['VIV_INTER'] == '1').astype(int)
            
            for reg_code, reg_name in [('01', 'AND'), (None, 'ESP')]:
                sub = df_valid[df_valid['CCAA'] == reg_code] if reg_code else df_valid
                # Ensure we have data
                if sub.empty: continue
                pct = (sub['TIENE_INTERNET'] * sub['FACTOR_H']).sum() / sub['FACTOR_H'].sum() * 100
                resultados.append({'Fecha': pd.to_datetime(f"{anio}-01-01"), 'Periodo': f"{anio}-ANUAL", 'Region': reg_name, 'Indicador': 'Acceso_Internet_Hogares', 'Valor': pct, 'Frecuencia': 'Anual', 'Serie_Original': fname})

    # Process TAB formats (2019-2025)
    for anio in range(2019, 2026):
        path = os.path.join(base_path, f"TICHcuestionario_{anio}.tab")
        if os.path.exists(path):
            df_y = pd.read_csv(path, sep='\t', dtype=str)
            df_y['FACTOR_H'] = pd.to_numeric(df_y['FACTOR_H'], errors='coerce')
            df_valid = df_y[df_y['VIV_INTER'].isin(['1', '6'])].copy()
            df_valid['TIENE_INTERNET'] = (df_valid['VIV_INTER'] == '1').astype(int)
            
            for reg_code, reg_name in [('01', 'AND'), (None, 'ESP')]:
                sub = df_valid[df_valid['CCAA'] == reg_code] if reg_code else df_valid
                if sub.empty: continue
                pct = (sub['TIENE_INTERNET'] * sub['FACTOR_H']).sum() / sub['FACTOR_H'].sum() * 100
                resultados.append({'Fecha': pd.to_datetime(f"{anio}-01-01"), 'Periodo': f"{anio}-ANUAL", 'Region': reg_name, 'Indicador': 'Acceso_Internet_Hogares', 'Valor': pct, 'Frecuencia': 'Anual', 'Serie_Original': f"TICHcuestionario_{anio}.tab"})

    if not resultados: return None
    df = pd.DataFrame(resultados).sort_values(['Region', 'Fecha'])
    path = os.path.join(DATA_PROCESSED, "Acceso_Internet_Hogares.csv")
    df.to_csv(path, index=False)
    print(f"   ✅ Saved: Acceso_Internet_Hogares.csv ({len(df)} records)")
    return df

def extract_broadband():
    """Extracts Annual Broadband Access for all regions from table 76594."""
    # Table 76594: Evolution of Housing data (2006-2025)
    # Check if we have a local JSON file to bypass SSL issues
    json_path = os.path.join(DATA_RAW, "76594.json")
    if os.path.exists(json_path):
        print(f"📂 Loading Broadband data from local JSON: {json_path}")
        import json
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Use IneConnector's logic but with provided data
            records = []
            from .config import REGIONS
            for serie in data:
                serie_name = serie['Nombre']
                if 'Banda Ancha' not in serie_name: continue
                
                region = None
                serie_name_upper = serie_name.upper()
                for code, name in REGIONS.items():
                    if name.upper() in serie_name_upper:
                        region = code
                        break
                    short_name = name.split(' de ')[-1].split(' Foral ')[-1].upper()
                    if short_name in serie_name_upper:
                        region = code
                        break
                if not region: continue
                
                for d in serie['Data']:
                    # Support both timestamp ('Fecha') and year strings ('Anyo')
                    if 'Fecha' in d:
                        fecha = pd.to_datetime(d['Fecha'], unit='ms')
                    else:
                        fecha = pd.to_datetime(f"{d['Anyo']}-01-01")
                        
                    records.append({
                        'Fecha': fecha,
                        'Periodo': f"{fecha.year}-ANUAL",
                        'Region': region,
                        'Indicador': 'Banda_Ancha',
                        'Valor': d['Valor'],
                        'Frecuencia': 'Anual',
                        'Serie_Original': serie_name
                    })
            if records:
                df = pd.DataFrame(records).drop_duplicates(subset=['Periodo', 'Region', 'Indicador']).sort_values(['Region', 'Fecha'])
            else:
                print("⚠️ No Broadband records found in local JSON.")
                df = None
    else:
        # Normal fallback to API if possible
        df = ine.download_tempus("76594", "Banda_Ancha")
        if df is not None:
            df = df[df['Serie_Original'].str.contains("Banda Ancha", case=False)]
            
    if df is not None:
        path = os.path.join(DATA_PROCESSED, "Banda_Ancha.csv")
        df.to_csv(path, index=False)
        print(f"   ✅ Saved: Banda_Ancha.csv ({len(df)} records)")
    return df

def extract_crime():
    """Downloads and processes quarterly crime data from the Ministry of Interior."""
    base_url = "https://estadisticasdecriminalidad.ses.mir.es/sec/jaxiPx/files/_px/es/csv_bdsc"
    q_map = {1: '001', 2: '004', 3: '007', 4: '010'}
    
    all_regs = []
    for year in range(2022, 2026):
        for q in [1, 2, 3, 4]:
            if year == 2025 and q > 2: continue
            
            suffix = q_map[q]
            if year == 2025: url = f"{base_url}/DatosBalanceAct/l0/09{suffix}.csv_bdsc?nocab=1"
            else: 
                y_code = year - 2010
                url = f"{base_url}/DatosBalanceAnt/l0/{y_code}09{suffix}.csv_bdsc?nocab=1"
            
            try:
                r = requests.get(url, timeout=15, verify=False)
                if r.status_code == 200:
                    df = pd.read_csv(io.BytesIO(r.content), sep=';', encoding='latin1', on_bad_lines='skip')
                    df.columns = [str(c).strip().lower() for c in df.columns]
                    
                    col_region = next((c for c in df.columns if 'comunid' in c), None)
                    col_total = next((c for c in df.columns if 'total' in c), None)
                    col_tipo = next((c for c in df.columns if 'tipolog' in c), None)
                    col_periodo = next((c for c in df.columns if 'periodo' in c), None)
                    
                    if all([col_region, col_total, col_tipo, col_periodo]):
                        sub = df[df[col_periodo].str.contains(str(year), na=False)]
                        from .config import REGIONS
                        for _, row in sub.iterrows():
                            reg_raw = str(row[col_region]).upper()
                            region = None
                            for code, name in REGIONS.items():
                                if name.upper() in reg_raw:
                                    region = code
                                    break
                            
                            if not region: continue
                            
                            val = str(row[col_total]).replace('.', '').replace(',', '.')
                            all_regs.append({
                                'Año': year, 'Trimestre': q, 'Region': region,
                                'Categoria': str(row[col_tipo]).strip(),
                                'Valor_Acumulado': float(val),
                                'Periodo': f"{year}-Q{q}"
                            })
            except: continue

    if not all_regs: return None
    df_acum = pd.DataFrame(all_regs)
    
    df_acum = df_acum.sort_values(['Region', 'Categoria', 'Año', 'Trimestre'])
    df_acum['Valor_Trimestral'] = df_acum.groupby(['Region', 'Categoria', 'Año'])['Valor_Acumulado'].diff().fillna(df_acum['Valor_Acumulado'])
    
    path = os.path.join(DATA_PROCESSED, "Criminalidad_Full.csv")
    df_acum.to_csv(path, index=False)
    print(f"   ✅ Saved: Criminalidad_Full.csv ({len(df_acum)} records)")
    return df_acum
