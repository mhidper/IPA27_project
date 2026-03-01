import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
nb_path = 'G:/Mi unidad/Proyectos/IPA27_project/notebooks/02_procesamiento_IPA27_CCAA.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if "INVERTIR =" in source:
             lines = source.split('\n')
             for line in lines:
                  if "INVERTIR =" in line:
                       print(line)
