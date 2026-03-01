import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
nb_path = 'G:/Mi unidad/Proyectos/IPA27_project/notebooks/02_procesamiento_IPA27_CCAA.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = cell['source']
        
        # 1. Quitar VID_ARO y VID_PAR de la lista de INVERTIR
        if "INVERTIR =" in "".join(source):
            new_lines = []
            for line in source:
                if "INVERTIR =" in line:
                    # Remplazos cuidadosos
                    line = line.replace("'VID_ARO', ", "").replace(", 'VID_ARO'", "").replace("'VID_ARO'", "")
                    line = line.replace("'VID_PAR', ", "").replace(", 'VID_PAR'", "").replace("'VID_PAR'", "")
                    new_lines.append(line)
                else:
                    new_lines.append(line)
            cell['source'] = new_lines
        
        # 2. Transformar VID_ARO y VID_PAR = 100 - x junto a EDU_ABA
        if "CARGA DE DATOS (Multiregional)" in "".join(source):
            new_lines = []
            for line in source:
                # Modificamos la transformación que hicimos de EDU_ABA para incluir los nuevos
                if "cols_edu =" in line:
                    new_lines.append("    cols_transform = [c for c in anual.columns if c.startswith('EDU_ABA_') or c.startswith('VID_ARO_')]\n")
                elif "for col in cols_edu:" in line:
                    new_lines.append("    for col in cols_transform:\n")
                elif "anual[col] = 100 - anual[col]" in line:
                    new_lines.append("        anual[col] = 100 - anual[col]\n")
                elif "if cols_edu: print(f\"\\n✓ EDU_ABA transformado a 'Positivo'" in line:
                    new_lines.append("    if cols_transform: print(f\"\\n✓ EDU_ABA y VID_ARO transformados a 'Positivo' (100 - x).\")\n")
                    
                    # Añadir transformación para trimestrales (VID_PAR está en trimestral)
                    new_lines.append("\n    # Transformación VID_PAR (Trimestral)\n")
                    new_lines.append("    cols_trim = [c for c in trimestral.columns if c.startswith('VID_PAR_')]\n")
                    new_lines.append("    for col in cols_trim:\n")
                    new_lines.append("        trimestral[col] = 100 - trimestral[col]\n")
                    new_lines.append("    if cols_trim: print(f\"✓ VID_PAR transformado a 'Positivo' (100 - x) para {len(cols_trim)} regiones.\\n\")\n")
                
                # Eliminamos las menciones antiguas de EDU_ABA por si interfieren
                elif "# === TRANSFORMACIÓN EXCEPCIONAL EDU_ABA ===" in line:
                    new_lines.append("\n# === TRANSFORMACIONES EXCEPCIONALES A 'POSITIVOS' ===\n")
                elif "# Convertimos 'Tasa de Abandono' en '% Población que completa estudios' (100 - x)" in line:
                    new_lines.append("# Convertimos 'Tasa de Abandono', 'Riesgo Pobreza' y 'Paro' en tasas de población positiva (100 - x)\n")
                    
                else:
                    new_lines.append(line)
            cell['source'] = new_lines

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("VID_ARO and VID_PAR transformations applied successfully.")
