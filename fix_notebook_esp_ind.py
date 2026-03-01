import json

nb_path = 'G:/Mi unidad/Proyectos/IPA27_project/notebooks/02_procesamiento_IPA27_CCAA.ipynb'
try:
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            lines = cell['source']
            for i, line in enumerate(lines):
                if '"pilares": {p: round(df_pilares.loc[last_q, f\'{p}_ESP\'], 1) for d in estructura.values() for p in d.keys()},' in line:
                    if lines[i+1].strip() == '}':
                        # Missing indicadores line, add it
                        lines[i] = line + '\n'
                        lines.insert(i+1, "            \"indicadores\": {ind: round(df_norm.loc[last_q, f'{ind}_ESP'], 1) for d in estructura.values() for p in d.values() for ind in p}\n")
                        print("Appended indicadores to ESP export.")
                        break

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
except Exception as e:
    print(e)
