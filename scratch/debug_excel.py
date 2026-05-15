import pandas as pd
import os

new_file = r"g:\Mi unidad\Proyectos\IPA27_project\results\data\ipa27_raw_20260510.xlsx"

if os.path.exists(new_file):
    xl = pd.ExcelFile(new_file)
    print(f"Hojas: {xl.sheet_names[:5]} ... (total {len(xl.sheet_names)})")
    if len(xl.sheet_names) > 1:
        sheet = xl.sheet_names[1]
        df = pd.read_excel(xl, sheet_name=sheet, nrows=5)
        print(f"\nEstructura de la hoja '{sheet}':")
        print(df.head())
        print(f"\nColumnas reales: {list(df.columns)}")
else:
    print("El archivo no existe.")
