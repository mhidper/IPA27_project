import pandas as pd
import os

old_file = r"g:\Mi unidad\Proyectos\IPA27_project\results\data\ipa27_raw_20260302.xlsx"
new_file = r"g:\Mi unidad\Proyectos\IPA27_project\results\data\ipa27_raw_20260510.xlsx"

def analyze_excel(path):
    if not os.path.exists(path): return None
    xl = pd.ExcelFile(path)
    summary = {}
    for sheet in xl.sheet_names:
        if sheet.upper() == 'LEER': continue
        try:
            df = pd.read_excel(xl, sheet_name=sheet, usecols=['Periodo'])
            max_p = df['Periodo'].max()
            summary[sheet] = {'max_p': max_p}
        except: continue
    return summary

print("--- AUDITORIA FINAL IPA27 ---")
old_s = analyze_excel(old_file)
new_s = analyze_excel(new_file)

if old_s and new_s:
    all_sheets = sorted(list(set(old_s.keys()) | set(new_s.keys())))
    print(f"{'Indicador':<15} | {'Anterior':<12} | {'Nuevo':<12} | {'Estado'}")
    print("-" * 75)
    for s in all_sheets:
        o = old_s.get(s, {'max_p': 'N/A'})
        n = new_s.get(s, {'max_p': 'N/A'})
        o_p = str(o['max_p'])
        n_p = str(n['max_p'])
        
        status = "SIN CAMBIOS"
        if n_p != "N/A":
            if o_p == "N/A": status = "NUEVO"
            elif n_p > o_p: status = "ACTUALIZADO"
            elif n_p < o_p: status = "REGRESION"
        
        if s not in new_s: status = "DESAPARECIDO"
        
        print(f"{s:<15} | {o_p:<12} | {n_p:<12} | {status}")
else:
    print("No se pudieron cargar los archivos.")
