import json

nb_path = 'G:/Mi unidad/Proyectos/IPA27_project/notebooks/02_procesamiento_IPA27_CCAA.ipynb'
try:
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    changed = False
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            for i, line in enumerate(cell['source']):
                if "'../dashboard/public/data/dashboard_data.json'" in line:
                    cell['source'][i] = line.replace("'../dashboard/public/data/dashboard_data.json'", "'dashboard/public/data/dashboard_data.json'")
                    changed = True

    if changed:
        with open(nb_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
        print("Path successfully fixed in Notebook.")
    else:
        print("Path not found, maybe already fixed?")
except Exception as e:
    print("Error:", e)
