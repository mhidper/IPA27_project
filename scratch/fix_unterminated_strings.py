import json
import os
import shutil

def fix_notebook_file(path):
    backup_path = path + '.bak'
    print(f"Procesando {path}...")
    
    with open(path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
        
    patched = False
    for cell in notebook.get('cells', []):
        if cell.get('cell_type') == 'code':
            source = cell.get('source', [])
            new_source = []
            i = 0
            cell_changed = False
            while i < len(source):
                current_line = source[i]
                # Búsqueda más robusta: f_out.write(f" e \newcommand
                if 'f_out.write(f"' in current_line and '\\newcommand' in current_line:
                    # Verificar si no está cerrado en la misma línea
                    stripped = current_line.strip()
                    if not (stripped.endswith('")') or stripped.endswith('")\n') or stripped.endswith('")\r\n')):
                        if i + 1 < len(source):
                            next_line = source[i+1]
                            if next_line.strip() in ['")', '")\n', '")\r\n']:
                                # Unirlas
                                merged_line = current_line.rstrip('\n').rstrip('\r') + '\\n")\n'
                                new_source.append(merged_line)
                                i += 2
                                cell_changed = True
                                print(f"  Parcheada línea: {current_line.strip()} con {next_line.strip()}")
                                continue
                new_source.append(current_line)
                i += 1
            if cell_changed:
                cell['source'] = new_source
                patched = True
                
    if patched:
        # Hacer copia de seguridad si no existe
        if not os.path.exists(backup_path):
            shutil.copy2(path, backup_path)
            print(f"Copia de seguridad creada en {backup_path}")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1, ensure_ascii=False)
        print(f"[OK] {path} corregido con éxito.")
    else:
        print(f"No se requirieron correcciones en {path}.")

if __name__ == '__main__':
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(project_root)
    fix_notebook_file('notebooks/02_3_exportacion.ipynb')
    print("-" * 50)
    fix_notebook_file('notebooks/02_procesamiento_IPA27_CCAA.ipynb')
