import requests
import pandas as pd
from datetime import datetime
import os
import io
from .config import DATA_PROCESSED
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class IneConnector:
    """Robust connector for INE (Spain) API (TEMPUS) and JAXI system."""
    
    def __init__(self):
        self.base_url = "https://servicios.ine.es/wstempus/js/ES/"
        self.jaxi_base_urls = [
            "https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/",
            "https://www.ine.es/jaxiT3/files/t/csv_bdsc/",
            "https://www.ine.es/jaxiT3/files/t/es/csv/"
        ]

    def _detect_frequency(self, serie_data):
        if not serie_data or len(serie_data) < 2:
            return "Anual"
        
        # Parse timestamps and check intervals
        dates = sorted([datetime.fromtimestamp(d['Fecha'] / 1000) for d in serie_data])
        diffs = [(dates[i+1] - dates[i]).days for i in range(min(len(dates)-1, 20))]
        avg_days = sum(diffs) / len(diffs) if diffs else 365
        
        if avg_days <= 35: return "Mensual"
        if avg_days <= 100: return "Trimestral"
        return "Anual"

    def download_tempus(self, table_id, name, start_date="20150101"):
        """Downloads data from INE TEMPUS API."""
        url = f"{self.base_url}DATOS_TABLA/{table_id}?date={start_date}:"
        print(f"⬇️ Downloading INE Table {table_id} ({name})...")
        
        try:
            resp = requests.get(url, timeout=30, verify=False)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"❌ Error downloading {table_id}: {e}")
            return None

        from .config import REGIONS
        
        records = []
        for serie in data:
            # Determine region dynamically from config.REGIONS
            region = None
            serie_name_upper = serie['Nombre'].upper()
            
            for code, name in REGIONS.items():
                # Special cases for names that might vary in JAXI/Tempus
                if name.upper() in serie_name_upper:
                    region = code
                    break
                # Fallback for short names if long name in config doesn't match exactly
                short_name = name.split(' de ')[-1].split(' Foral ')[-1].upper()
                if short_name in serie_name_upper:
                    region = code
                    break
            
            if not region: continue
            
            freq = self._detect_frequency(serie['Data'])
            for d in serie['Data']:
                dt = datetime.fromtimestamp(d['Fecha'] / 1000)
                
                if freq == "Mensual":
                    period = f"{dt.year}-M{dt.month:02d}"
                elif freq == "Trimestral":
                    period = f"{dt.year}-Q{(dt.month-1)//3 + 1}"
                else:
                    period = f"{dt.year}-ANUAL"
                
                records.append({
                    'Fecha': dt,
                    'Periodo': period,
                    'Region': region,
                    'Indicador': name,
                    'Valor': d['Valor'],
                    'Frecuencia': freq,
                    'Serie_Original': serie['Nombre']
                })
        
        if not records:
            print(f"⚠️ No valid series found for {table_id}")
            return None
            
        df = pd.DataFrame(records)
        if 'Region' in df.columns:
            df = df.drop_duplicates(subset=['Periodo', 'Region', 'Indicador']).sort_values('Fecha')
        
        path = os.path.join(DATA_PROCESSED, f"{name}.csv")
        df.to_csv(path, index=False)
        print(f"   ✅ Saved: {name}.csv ({len(df)} records)")
        return df

    def download_jaxi(self, table_id, name, filter_keyword=None):
        """Downloads data from INE JAXI system (static CSV files)."""
        print(f"⬇️ Downloading JAXI Table {table_id} ({name})... ")
        df_raw = None
        for base in self.jaxi_base_urls:
            try:
                url = f"{base}{table_id}.csv"
                r = requests.get(url, timeout=30, verify=False)
                if r.status_code == 200:
                    # JAXI often uses latin-1 or ISO-8859-15 encoding
                    content = r.content.decode('ISO-8859-15')
                    df_raw = pd.read_csv(io.StringIO(content), sep=';', decimal=',', encoding='utf-8')
                    break
            except: continue
            
        if df_raw is None:
            print(f"❌ Failed to download JAXI {table_id}")
            return None
            
        # Process JAXI matrix format: Years are usually the columns, first col is description
        year_cols = [c for c in df_raw.columns if str(c).strip().isdigit() and len(str(c).strip()) == 4]
        desc_col = df_raw.columns[0]
        
        records = []
        for _, row in df_raw.iterrows():
            desc = str(row[desc_col])
            if filter_keyword and filter_keyword.lower() not in desc.lower(): continue
            
            from .config import REGIONS
            row_desc_upper = desc.upper()
            region = None
            for code, name in REGIONS.items():
                if name.upper() in row_desc_upper:
                    region = code
                    break
                short_name = name.split(' de ')[-1].split(' Foral ')[-1].upper()
                if short_name in row_desc_upper:
                    region = code
                    break
            
            if not region: continue
            
            for y in year_cols:
                val_raw = str(row[y]).replace('.', '').replace(',', '.').strip()
                try:
                    val = float(val_raw)
                    records.append({
                        'Fecha': pd.to_datetime(f"{y}-01-01"),
                        'Periodo': f"{y}-ANUAL",
                        'Region': region,
                        'Indicador': name,
                        'Valor': val,
                        'Frecuencia': 'Anual',
                        'Serie_Original': desc.strip()
                    })
                except: continue
                
        if not records:
            print(f"⚠️ No records extracted from JAXI {table_id}")
            return None
            
        df = pd.DataFrame(records)
        if 'Region' in df.columns:
             df = df.drop_duplicates(subset=['Periodo', 'Region', 'Indicador']).sort_values('Fecha')
        
        path = os.path.join(DATA_PROCESSED, f"{name}.csv")
        df.to_csv(path, index=False)
        print(f"   ✅ Saved: {name}.csv ({len(df)} records)")
        return df

    def download_jaxi_long(self, table_ids, name, filters=None):
        """
        Downloads data from INE JAXI where years/periods are in a column (long format).
        table_ids: dict like {'ESP': '27153', 'AND': '27154'} OR single ID string for shared tables.
        """
        if isinstance(table_ids, str):
            table_ids = {'ESP': table_ids, 'AND': table_ids}
            
        print(f"⬇️ Downloading JAXI Multi-Table ({name})...")
        records = []
        
        for region, tid in table_ids.items():
            print(f"   🔄 [{region}] Downloading Table {tid}...")
            df_raw = None
            for base in self.jaxi_base_urls:
                try:
                    url = f"{base}{tid}.csv"
                    r = requests.get(url, timeout=30, verify=False)
                    if r.status_code == 200:
                        content = r.content.decode('ISO-8859-15')
                        df_raw = pd.read_csv(io.StringIO(content), sep=';', encoding='utf-8')
                        break
                except: continue
            
            if df_raw is None:
                print(f"   ❌ Failed to download {region} table {tid}")
                continue
                
            # Apply filters
            df_filt = df_raw.copy()
            if filters:
                for col_key, val in filters.items():
                    col_actual = next((c for c in df_filt.columns if col_key.lower() in c.lower()), None)
                    if col_actual:
                        df_filt = df_filt[df_filt[col_actual].astype(str).str.contains(val, case=False, na=False)]
            
            # Find Period and Value columns
            col_period = next((c for c in df_filt.columns if 'periodo' in c.lower()), None)
            col_value = next((c for c in df_filt.columns if 'total' in c.lower()), None)
            
            if not col_period or not col_value:
                print(f"   ⚠️ Row-based columns not found for {region}")
                continue
                
            for _, row in df_filt.iterrows():
                try:
                    p_str = str(row[col_period]).strip()
                    if not p_str.isdigit(): continue
                    year = int(p_str)
                    val = float(str(row[col_value]).replace(',', '.').strip())
                    
                    records.append({
                        'Fecha': pd.to_datetime(f"{year}-01-01"),
                        'Periodo': f"{year}-ANUAL",
                        'Region': region,
                        'Indicador': name,
                        'Valor': val,
                        'Frecuencia': 'Anual',
                        'Serie_Original': f"{name}_{region}"
                    })
                except: continue
                
        if not records:
            print(f"   ⚠️ No records extracted for {name}")
            return None
            
        df = pd.DataFrame(records)
        if 'Region' in df.columns:
            df = df.drop_duplicates(subset=['Periodo', 'Region', 'Indicador']).sort_values('Fecha')
        
        path = os.path.join(DATA_PROCESSED, f"{name}.csv")
        df.to_csv(path, index=False)
        print(f"   ✅ Saved: {name}.csv ({len(df)} records)")
        return df
