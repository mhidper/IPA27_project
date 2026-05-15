import requests
import pandas as pd
import urllib3
import json

# Desactivar warnings de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DebugIECA:
    def __init__(self):
        self.base_url = "https://www.juntadeandalucia.es/institutodeestadisticaycartografia/intranet/admin/rest/v1.0"
        self.timeout = 30
        self.consulta_id = "106151"

    def debug_pib(self):
        print(f"--- Debugging Consulta {self.consulta_id} ---")
        
        # 1. Obtener Metadatos
        try:
            meta_url = f"{self.base_url}/consulta/{self.consulta_id}"
            print(f"Fetching metadata from: {meta_url}")
            meta = requests.get(meta_url, timeout=self.timeout, verify=False).json()
            
            # Ver dimensiones disponibles
            print("\nDimensiones encontradas:")
            for h in meta.get('hierarchies', []):
                print(f" - Alias: {h.get('alias')}, URL: {h.get('url')}")
            
            temp_hier = next((h for h in meta['hierarchies'] if h['alias'] == 'D_TEMPORAL_0'), None)
            if not temp_hier:
                print("(!) No se encontró la jerarquía D_TEMPORAL_0")
                return

            # 2. Verificar componentes
            comp_hier = next((h for h in meta['hierarchies'] if h['alias'] == 'D_CRTA_COMPONPIB2008_0'), None)
            if comp_hier:
                print(f"\nFetching component hierarchy from: {comp_hier['url']}")
                comp_data = requests.get(comp_hier['url'], timeout=self.timeout, verify=False).json()
                
                all_comps = []
                def extract_comps(item):
                    all_comps.append({'id': item.get('id'), 'cod': item.get('cod'), 'label': item.get('label')})
                    for child in item.get('children', []): extract_comps(child)
                
                extract_comps(comp_data.get('data', {}))
                df_comp = pd.DataFrame(all_comps)
                print("\nPrimeros 20 componentes encontrados:")
                print(df_comp.head(20))
                
                pib_match = df_comp[df_comp['label'].str.contains("Producto Interior Bruto", na=False)]
                if not pib_match.empty:
                    print("\nIDs de PIB encontrados:")
                    print(pib_match)
                else:
                    print("\n(!) No se encontro 'Producto Interior Bruto' en los componentes.")

            # 2.7 Verificar territorio
            terr_hier = next((h for h in meta['hierarchies'] if h['alias'] == 'D_TERRITORIO_0'), None)
            if terr_hier:
                print(f"\nFetching territory hierarchy from: {terr_hier['url']}")
                terr_data = requests.get(terr_hier['url'], timeout=self.timeout, verify=False).json()
                all_terr = []
                def extract_terr(item):
                    all_terr.append({'id': item.get('id'), 'cod': item.get('cod'), 'label': item.get('label')})
                    for child in item.get('children', []): extract_terr(child)
                extract_terr(terr_data.get('data', {}))
                print("\nTerritorios encontrados:")
                print(pd.DataFrame(all_terr))
            print(f"\nFetching temporal hierarchy from: {temp_hier['url']}")
            jer_data = requests.get(temp_hier['url'], timeout=self.timeout, verify=False).json()
            
            all_temporal_codes = []
            def extract_info(item, level=0):
                cod = str(item.get('cod', ''))
                label = item.get('label', '')
                level_id = item.get('levelId')
                
                if level_id == 3:
                    all_temporal_codes.append({'id': item.get('id'), 'cod': cod, 'label': label})
                
                children = item.get('children', [])
                for child in children:
                    extract_info(child, level + 1)

            extract_info(jer_data.get('data', {}))
            
            df_temp = pd.DataFrame(all_temporal_codes)
            if not df_temp.empty:
                print(f"\nTotal de códigos temporales encontrados: {len(df_temp)}")
                df_temp['anio'] = df_temp['cod'].str[:4].astype(int)
                df_temp['trimestre'] = df_temp['cod'].str[4:].astype(int)
                
                print("\nResumen por años (top 5 más recientes):")
                print(df_temp.sort_values(['anio', 'trimestre'], ascending=False).head(10))
                
                # Buscar específicamente 2025 y 2026
                recientes = df_temp[df_temp['anio'] >= 2024]
                if not recientes.empty:
                    print("\nRegistros de 2024 en adelante:")
                    print(recientes.sort_values(['anio', 'trimestre']))
                else:
                    print("(!) No se encontraron registros de 2024 o posteriores en esta consulta.")

            # 3. Intentar consulta de datos
            # Usamos los últimos 5 IDs cronológicos para probar
            if not df_temp.empty:
                # Usamos los IDs de 2024 y 2025
                recent_mask = (df_temp['anio'] >= 2024) & (df_temp['anio'] <= 2026)
                ids_test = df_temp[recent_mask]['id'].astype(str).tolist()
                ids_str = ",".join(ids_test)
                
                data_url = f"{self.base_url}/consulta/{self.consulta_id}?D_CRTA_COMPONPIB2008_0=69618&D_TEMPORAL_0={ids_str}&D_TERRITORIO_0=21&D_CRTA_SERIE_0=1"
                print(f"\nFetching data from: {data_url}")
                res = requests.get(data_url, timeout=self.timeout, verify=False).json()
                
                print("\nResultados de la consulta:")
                data = res.get('data', [])
                if not data:
                    print("(!) La consulta no devolvio datos para estos IDs.")
                for item in data:
                    # Estructura IECA: [ [index], [temporal], [componente], [unidad], [valor_obj] ]
                    # item[1] es temporal, item[4] es el valor
                    try:
                        t_cod = item[1]['cod'][0]
                        val = item[4].get('val')
                        print(f" - Temporal: {t_cod}, Valor: {val}")
                    except:
                        print(f" - Error parseando item: {item}")
            else:
                print("(X) No hay IDs para probar consulta.")

        except Exception as e:
            print(f"(X) Error durante el debug: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    debugger = DebugIECA()
    debugger.debug_pib()
