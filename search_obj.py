import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

nb_path = 'G:/Mi unidad/Proyectos/IPA27_project/notebooks/02_procesamiento_IPA27_CCAA.ipynb'
try:
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source'])
            if '2025Q3' in source or 'OBJETIVO' in source:
                lines = source.split('\n')
                for j, line in enumerate(lines):
                    if '2025Q3' in line or 'OBJETIVO' in line:
                        print(f"Cell {i}, Line {j}: {line.strip()[:150]}")
except Exception as e:
    print(f"Error {e}")
