import json

nb_path = 'G:/Mi unidad/Proyectos/IPA27_project/notebooks/02_procesamiento_IPA27_CCAA.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if "export_dashboard_data(" in source:
            print("FOUND export_dashboard_data!")
            print(source)
