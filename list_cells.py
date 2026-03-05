import json
nb_path = r'g:\Mi unidad\Proyectos\IPA27_project\notebooks\02_procesamiento_IPA27_CCAA.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i in range(40, 48):
    cell = nb['cells'][i]
    source = ''.join(cell['source'])
    print(f"Cell {i} (Type: {cell['cell_type']}): {repr(source[:60])}")
