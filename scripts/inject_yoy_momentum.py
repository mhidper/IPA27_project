import json
import os

nb_path = r'g:\Mi unidad\Proyectos\IPA27_project\notebooks\02_procesamiento_IPA27_CCAA.ipynb'

NEW_ANALYSIS_CELL = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# =============================================================================\n",
        "# 7. ANÁLISIS DE MOMENTUM (CONTRIBUCIONES YoY)\n",
        "# =============================================================================\n",
        "print(\"📊 7/7 Generando: Análisis de Momentum (Variación Interanual YoY)...\")\n",
        "\n",
        "import numpy as np\n",
        "import matplotlib.pyplot as plt\n",
        "import pandas as pd\n",
        "\n",
        "# 1. Análisis de contribuciones exactas a la media geométrica (Descomposición Logarítmica)\n",
        "# Seleccionamos la región de análisis (Andalucía)\n",
        "region = 'AND'\n",
        "col_ipa = f'IPA27_{region}'\n",
        "dominios = list(ESTRUCTURA.keys())\n",
        "cols_dominios = [f'{d}_{region}' for d in dominios]\n",
        "\n",
        "# Variación interanual (4 trimestres para YoY)\n",
        "df_ipa_yoy = df_ipa27[[col_ipa]].diff(4)\n",
        "\n",
        "# Función de peso de atribución W = (I_t - I_{t-4}) / (ln(I_t) - ln(I_{t-4}))\n",
        "def calc_w(val_t, val_t4):\n",
        "    if pd.isna(val_t) or pd.isna(val_t4):\n",
        "        return np.nan\n",
        "    if abs(val_t - val_t4) < 1e-6:\n",
        "        return val_t\n",
        "    return (val_t - val_t4) / (np.log(val_t) - np.log(val_t4))\n",
        "\n",
        "contribuciones = []\n",
        "\n",
        "for t in df_ipa27.index[4:]:  # Empezamos desde el 5to periodo para tener t-4\n",
        "    ipa_t = df_ipa27.loc[t, col_ipa]\n",
        "    ipa_t4 = df_ipa27.shift(4).loc[t, col_ipa]\n",
        "    \n",
        "    w = calc_w(ipa_t, ipa_t4)\n",
        "    \n",
        "    fila = {'Trimestre': t, 'Variacion_Total': ipa_t - ipa_t4}\n",
        "    \n",
        "    # Contribución de cada dominio\n",
        "    for dom, col_d in zip(dominios, cols_dominios):\n",
        "        d_t = df_dominios.loc[t, col_d]\n",
        "        d_t4 = df_dominios.shift(4).loc[t, col_d]\n",
        "        \n",
        "        if pd.notna(d_t) and pd.notna(d_t4) and d_t > 0 and d_t4 > 0:\n",
        "            # Peso igual (1/3) porque es equiponderado\n",
        "            c_dom = w * (1/3) * (np.log(d_t) - np.log(d_t4))\n",
        "            fila[dom] = c_dom\n",
        "        else:\n",
        "            fila[dom] = np.nan\n",
        "            \n",
        "    contribuciones.append(fila)\n",
        "\n",
        "df_contrib = pd.DataFrame(contribuciones).set_index('Trimestre')\n",
        "\n",
        "# 2. Visualización: Gráfico de Barras Apiladas + Línea\n",
        "fig, ax = plt.subplots(figsize=(14, 8))\n",
        "\n",
        "# Definir colores para cada dominio\n",
        "colores = {'ECO': '#007932', 'SOC': '#A8DADC', 'GOB': '#F4A261'}\n",
        "\n",
        "trimestres = df_contrib.index\n",
        "x = np.arange(len(trimestres))\n",
        "\n",
        "# Separar contribuciones positivas y negativas para apilar correctamente\n",
        "bottom_pos = np.zeros(len(trimestres))\n",
        "bottom_neg = np.zeros(len(trimestres))\n",
        "\n",
        "for dom in dominios:\n",
        "    valores = df_contrib[dom].fillna(0).values\n",
        "    \n",
        "    val_pos = np.where(valores > 0, valores, 0)\n",
        "    val_neg = np.where(valores < 0, valores, 0)\n",
        "    \n",
        "    ax.bar(x, val_pos, bottom=bottom_pos, color=colores.get(dom, '#cccccc'), edgecolor='white', label=dom if x[0]==0 else \"\")\n",
        "    ax.bar(x, val_neg, bottom=bottom_neg, color=colores.get(dom, '#cccccc'), edgecolor='white')\n",
        "    \n",
        "    bottom_pos += val_pos\n",
        "    bottom_neg += val_neg\n",
        "\n",
        "# Línea de variación total del IPA27\n",
        "ax.plot(x, df_contrib['Variacion_Total'], color='black', marker='o', linewidth=2, markersize=8, label='Variación IPA27 YoY')\n",
        "\n",
        "# Formato\n",
        "ax.set_title(f'Evolución de Aportaciones al IPA27 (Variación Interanual - Andalucía)', fontsize=16, fontweight='bold', pad=20)\n",
        "ax.set_xticks(x)\n",
        "ax.set_xticklabels(trimestres, rotation=45, ha='right')\n",
        "ax.axhline(0, color='gray', linewidth=1)\n",
        "ax.set_ylabel('Variación Interanual (Puntos)', fontsize=12)\n",
        "\n",
        "# Leyenda sin duplicados\n",
        "handles, labels = ax.get_legend_handles_labels()\n",
        "by_label = dict(zip(labels, handles))\n",
        "ax.legend(by_label.values(), by_label.keys(), loc='upper left', bbox_to_anchor=(1, 1))\n",
        "\n",
        "plt.tight_layout()\n",
        "plt.savefig('results/figures/analysis/ipa27_contribuciones_yoy.png', dpi=150, bbox_inches='tight', facecolor='white')\n",
        "plt.show()\n",
        "\n",
        "print(f\"✓ Gráfico guardado: results/figures/analysis/ipa27_contribuciones_yoy.png\")\n"
    ]
}

try:
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # Reemplazar la celda actual de Momentum
    target_idx = -1
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown' and '# Análisis de Momentum' in "".join(cell['source']):
            target_idx = i
            break
            
    if target_idx != -1:
        # La siguiente celda es la de código, la reemplazamos
        nb['cells'][target_idx+1] = NEW_ANALYSIS_CELL
        print("Updated existing momentum analysis cell.")
    else:
        # Esto no debería pasar porque ya la insertaste antes
        print("Couldn't find target markdown cell. Creating it...")
        nb['cells'].append({"cell_type": "markdown", "metadata": {}, "source": ["# Análisis de Momentum\n"]})
        nb['cells'].append(NEW_ANALYSIS_CELL)

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    
    print("Notebook updated successfully.")

except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
