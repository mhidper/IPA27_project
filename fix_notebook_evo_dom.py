import json

nb_path = 'G:/Mi unidad/Proyectos/IPA27_project/notebooks/02_procesamiento_IPA27_CCAA.ipynb'
try:
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            lines = cell['source']
            for i, line in enumerate(lines):
                if '"esp_global": df_hist[\'IPA27_ESP\'].round(2).tolist()' in line:
                    lines[i] = line.replace('\n', '') + ',\n'
                    lines.insert(i+1, "        \"and_dominios\": {d: df_dominios.loc['2015Q1':][f'{d}_AND'].round(2).tolist() for d in estructura.keys()}\n")
                    print("Appended and_dominios to evolution export.")
                    break

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
except Exception as e:
    print(e)
