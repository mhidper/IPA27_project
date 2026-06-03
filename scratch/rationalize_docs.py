import os
import shutil
import json
import re

def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(project_root)
    print(f"Directorio de trabajo establecido en: {project_root}")
    
    # 1. Crear directorios objetivo
    dirs_to_create = [
        'docs/convenios',
        'docs/infografias',
        'docs/metodologia/01_general',
        'docs/metodologia/02_desafeccion',
        'docs/metodologia/03_participacion_electoral',
        'docs/metodologia/notas_trabajo'
    ]
    for d in dirs_to_create:
        os.makedirs(d, exist_ok=True)
        print(f"Directorio verificado/creado: {d}")
        
    # 2. Funciones auxiliares para mover ficheros
    def move_files_in_dir(src_dir, dst_dir):
        if not os.path.exists(src_dir):
            print(f"Origen no existe, omitiendo: {src_dir}")
            return
        for item in os.listdir(src_dir):
            s_path = os.path.join(src_dir, item)
            d_path = os.path.join(dst_dir, item)
            if os.path.isdir(s_path):
                # Omitimos notas si estamos en methodology
                if item == 'notes' and src_dir == 'docs/methodology':
                    continue
                shutil.copytree(s_path, d_path, dirs_exist_ok=True)
                shutil.rmtree(s_path)
                print(f"Directorio movido: {s_path} -> {d_path}")
            else:
                shutil.move(s_path, d_path)
                print(f"Fichero movido: {s_path} -> {d_path}")
                
    # 3. Mover ficheros según el plan
    print("\n--- MOVIENDO ARCHIVOS ---")
    
    # Mover docs/agreements a docs/convenios
    move_files_in_dir('docs/agreements', 'docs/convenios')
    if os.path.exists('docs/agreements'):
        os.rmdir('docs/agreements')
        print("Eliminado directorio vacio: docs/agreements")
        
    # Mover docs/convenios a docs/convenios (nada que hacer, ya se mueven ahi)
    
    # Mover docs/infographics a docs/infografias
    move_files_in_dir('docs/infographics', 'docs/infografias')
    if os.path.exists('docs/infographics'):
        os.rmdir('docs/infographics')
        print("Eliminado directorio vacio: docs/infographics")
        
    # Mover docs/methodology/notes a docs/metodologia/notas_trabajo
    move_files_in_dir('docs/methodology/notes', 'docs/metodologia/notas_trabajo')
    if os.path.exists('docs/methodology/notes'):
        os.rmdir('docs/methodology/notes')
        print("Eliminado directorio vacio: docs/methodology/notes")
        
    # Mover docs/methodology a docs/metodologia/01_general
    move_files_in_dir('docs/methodology', 'docs/metodologia/01_general')
    if os.path.exists('docs/methodology'):
        os.rmdir('docs/methodology')
        print("Eliminado directorio vacio: docs/methodology")
        
    # Mover metodologia/01_IPA27_General a docs/metodologia/01_general
    move_files_in_dir('metodologia/01_IPA27_General', 'docs/metodologia/01_general')
    if os.path.exists('metodologia/01_IPA27_General'):
        os.rmdir('metodologia/01_IPA27_General')
        print("Eliminado directorio vacio: metodologia/01_IPA27_General")
        
    # Mover metodologia/02_Indice_Desafeccion a docs/metodologia/02_desafeccion
    move_files_in_dir('metodologia/02_Indice_Desafeccion', 'docs/metodologia/02_desafeccion')
    if os.path.exists('metodologia/02_Indice_Desafeccion'):
        os.rmdir('metodologia/02_Indice_Desafeccion')
        print("Eliminado directorio vacio: metodologia/02_Indice_Desafeccion")
        
    # Mover metodologia/03_Participacion_Electoral a docs/metodologia/03_participacion_electoral
    move_files_in_dir('metodologia/03_Participacion_Electoral', 'docs/metodologia/03_participacion_electoral')
    if os.path.exists('metodologia/03_Participacion_Electoral'):
        os.rmdir('metodologia/03_Participacion_Electoral')
        print("Eliminado directorio vacio: metodologia/03_Participacion_Electoral")
        
    # Eliminar raiz metodologia/ si esta vacio
    if os.path.exists('metodologia'):
        try:
            os.rmdir('metodologia')
            print("Eliminado directorio raiz vacio: metodologia/")
        except OSError as e:
            print(f"Advertencia: No se pudo borrar metodologia/ porque no esta vacio: {e}")

    # 4. Modificar rutas relativas en archivos de texto
    print("\n--- MODIFICANDO RUTAS EN DOCUMENTOS ---")
    
    # presentacion_ipa27_v5.tex
    pres_tex = 'docs/metodologia/01_general/presentacion_ipa27_v5.tex'
    if os.path.exists(pres_tex):
        with open(pres_tex, 'r', encoding='utf-8') as f:
            content = f.read()
        # Cambiar ../../ por ../../../ en graphicspath
        target_str = r'\graphicspath{{../../results/figures/analysis/}{../../data/processed/cis/barómetro/}}'
        replacement_str = r'\graphicspath{{../../../results/figures/analysis/}{../../../data/processed/cis/barómetro/}}'
        if target_str in content:
            content = content.replace(target_str, replacement_str)
            with open(pres_tex, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Rutas de imagenes de presentacion actualizadas en: {pres_tex}")
        else:
            # Reemplazo por expresiones regulares mas flexible
            content_new, count = re.subn(r'\{\.\./\.\./results/', '{../../../results/', content)
            content_new, count2 = re.subn(r'\{\.\./\.\./data/', '{../../../data/', content_new)
            if count > 0 or count2 > 0:
                with open(pres_tex, 'w', encoding='utf-8') as f:
                    f.write(content_new)
                print(f"Rutas de imagenes actualizadas por regex ({count + count2} reemplazos) en: {pres_tex}")
            else:
                print(f"No se requirio actualizacion en: {pres_tex}")
                
    # ideas_fuerza_resultados.md
    ideas_md = 'docs/metodologia/01_general/ideas_fuerza_resultados.md'
    if os.path.exists(ideas_md):
        with open(ideas_md, 'r', encoding='utf-8') as f:
            content = f.read()
        # Cambiar ../../ por ../../../
        content_new, count = re.subn(r'\.\./\.\./results/', '../../../results/', content)
        if count > 0:
            with open(ideas_md, 'w', encoding='utf-8') as f:
                f.write(content_new)
            print(f"Enlaces de imagenes actualizados ({count} reemplazos) en: {ideas_md}")
            
    # methodology.tex
    methodology_tex = 'docs/metodologia/01_general/methodology.tex'
    if os.path.exists(methodology_tex):
        with open(methodology_tex, 'r', encoding='utf-8') as f:
            content = f.read()
        # Cambiar ../ipa27_ a ../../ipa27_
        content_new, count = re.subn(r'\{\.\./ipa27_', '{../../ipa27_', content)
        if count > 0:
            with open(methodology_tex, 'w', encoding='utf-8') as f:
                f.write(content_new)
            print(f"Rutas de imagenes actualizadas ({count} reemplazos) en: {methodology_tex}")

    # 5. Modificar notebooks
    print("\n--- MODIFICANDO NOTEBOOKS ---")
    notebooks = [
        'notebooks/02_3_exportacion.ipynb',
        'notebooks/02_procesamiento_IPA27_CCAA.ipynb'
    ]
    for nb_path in notebooks:
        if not os.path.exists(nb_path):
            print(f"Notebook no encontrado: {nb_path}")
            continue
        print(f"Leyendo {nb_path}...")
        with open(nb_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
            
        changed = False
        for cell in notebook.get('cells', []):
            new_source = []
            for line in cell.get('source', []):
                # Reemplazo de ruta
                if 'metodologia/01_IPA27_General/' in line:
                    line = line.replace('metodologia/01_IPA27_General/', 'docs/metodologia/01_general/')
                    changed = True
                new_source.append(line)
            cell['source'] = new_source
            
        if changed:
            with open(nb_path, 'w', encoding='utf-8') as f:
                json.dump(notebook, f, indent=1, ensure_ascii=False)
            print(f"[OK] Notebook actualizado con exito: {nb_path}")
        else:
            print(f"No se requirieron cambios en: {nb_path}")

if __name__ == '__main__':
    main()
