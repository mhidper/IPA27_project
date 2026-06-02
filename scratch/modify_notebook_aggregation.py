"""
Modifica la Celda 46 del notebook 02_procesamiento_IPA27_CCAA.ipynb
para cambiar el método de agregación jerárquica de Media Geométrica a Media Aritmética.
"""
import json
import sys

nb_path = r"g:\Mi unidad\Proyectos\IPA27_project\notebooks\02_procesamiento_IPA27_CCAA.ipynb"

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Buscamos la Celda 46 (Agregación)
target_idx = None
for idx, cell in enumerate(nb.get("cells", [])):
    if cell.get("cell_type") != "code":
        continue
    source = "".join(cell.get("source", []))
    if "AGREGACIÓN JERÁRQUICA (Media Geométrica)" in source or "AGREGACIÓN (Media Geométrica - IPA27)" in source:
        target_idx = idx
        break

if target_idx is not None:
    source_lines = nb["cells"][target_idx]["source"]
    new_lines = []
    
    # 1. Definición de la función media_aritmetica a insertar
    def_aritmetica = (
        "\n# === FUNCIÓN DE MEDIA ARITMÉTICA ROBUSTA ===\n"
        "def media_aritmetica(df_componentes, pesos=None):\n"
        "    \"\"\"\n"
        "    Calcula la media aritmética ponderada por filas, ignorando NaNs.\n"
        "    \"\"\"\n"
        "    if pesos is None:\n"
        "        pesos = {col: 1.0 for col in df_componentes.columns}\n"
        "    \n"
        "    resultado = pd.Series(index=df_componentes.index, dtype=float)\n"
        "    \n"
        "    for idx in df_componentes.index:\n"
        "        fila = df_componentes.loc[idx]\n"
        "        \n"
        "        # Filtrar NaNs\n"
        "        validos = fila.dropna()\n"
        "        \n"
        "        if len(validos) == 0:\n"
        "            resultado[idx] = np.nan\n"
        "            continue\n"
        "            \n"
        "        w = np.array([pesos.get(col, 1.0) for col in validos.index], dtype=float)\n"
        "        v = validos.values.astype(float)\n"
        "        \n"
        "        suma_pesos = w.sum()\n"
        "        if suma_pesos == 0:\n"
        "            resultado[idx] = np.nan\n"
        "            continue\n"
        "            \n"
        "        resultado[idx] = np.sum(w * v) / suma_pesos\n"
        "        \n"
        "    return resultado\n"
    )

    inserted_def = False
    for line in source_lines:
        # Reemplazar cabecera para reflejar media aritmética
        if "AGREGACIÓN JERÁRQUICA (Media Geométrica)" in line:
            line = line.replace("Media Geométrica", "Media Aritmética")
        elif "AGREGACIÓN (Media Geométrica - IPA27)" in line:
            line = line.replace("Media Geométrica - IPA27", "Media Aritmética - IPA27")
            
        new_lines.append(line)
        
        # Insertar la definición de media_aritmetica justo después de la definición de media_geometrica
        if "return resultado" in line and not inserted_def:
            # Encontrar si pertenece a la función media_geometrica (las primeras líneas)
            # Como la función media_geometrica termina con return resultado, insertamos después de la primera ocurrencia
            new_lines.append(def_aritmetica)
            inserted_def = True
            
        # Reemplazar las llamadas de agregación en los 3 niveles
        # Nivel 1 (Indicadores -> Pilares)
        if "df_pilares[col_pilar] = media_geometrica(df_norm[cols_disponibles])" in line:
            new_lines[-1] = line.replace("media_geometrica", "media_aritmetica")
            # Cambiar comentario de equiponderado
            if len(new_lines) >= 2 and "Media geométrica" in new_lines[-2]:
                new_lines[-2] = new_lines[-2].replace("Media geométrica", "Media aritmética")
                
        # Nivel 2 (Pilares -> Dominios)
        elif "df_dominios[col_dominio] = media_geometrica(df_pilares[cols_disponibles])" in line:
            new_lines[-1] = line.replace("media_geometrica", "media_aritmetica")
            
        # Nivel 3 (Dominios -> IPA27)
        elif "df_ipa27[col_ipa] = media_geometrica(df_dominios[cols_disponibles])" in line:
            new_lines[-1] = line.replace("media_geometrica", "media_aritmetica")
            
        # Cambiar el reporte final de consola del notebook
        elif "calculado con media geométrica para todas las regiones" in line:
            new_lines[-1] = line.replace("media geométrica", "media aritmética")

    nb["cells"][target_idx]["source"] = new_lines
    sys.stdout.buffer.write(f"[OK] Celda {target_idx} modificada con agregacion por media aritmetica.\n".encode())
else:
    sys.stdout.buffer.write(b"[ERROR] No se encontro la celda de agregacion en el notebook.\n")

with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

sys.stdout.buffer.write(b"Listo.\n")
