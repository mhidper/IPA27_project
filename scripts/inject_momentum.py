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
        "# 7. ANÁLISIS DE MOMENTUM (VARIACIÓN TRIMESTRAL)\n",
        "# =============================================================================\n",
        "print(\"📊 7/7 Generando: Análisis de Momentum (Variación Trimestral)...\")\n",
        "\n",
        "# 1. Calcular cambios absolutos (puntos) respecto al trimestre anterior\n",
        "df_cambio_global = df_ipa27.diff()\n",
        "df_cambio_dominios = df_dominios.diff()\n",
        "df_cambio_pilares = df_pilares.diff()\n",
        "\n",
        "# 2. Visualización de los últimos cambios en Andalucía\n",
        "ultimo_q = df_ipa27.index[-1]\n",
        "penultimo_q = df_ipa27.index[-2]\n",
        "\n",
        "# Definir etiquetas (Global, Dominios, Pilares)\n",
        "dominios_n = list(ESTRUCTURA.keys())\n",
        "# Extraer nombres limpios de los pilares (sin el prefijo de número)\n",
        "pilares_n = [p.split(\". \")[1] if \". \" in p else p for d in ESTRUCTURA.values() for p in d.keys()]\n",
        "\n",
        "# Recopilar datos de momentum para Andalucía\n",
        "momentum_and = {'Global (IPA27)': df_cambio_global.loc[ultimo_q, 'IPA27_AND']}\n",
        "\n",
        "for d in dominios_n:\n",
        "    momentum_and[d] = df_cambio_dominios.loc[ultimo_q, f\"{d}_AND\"]\n",
        "\n",
        "for p in pilares_n:\n",
        "    col = f\"{p}_AND\"\n",
        "    if col in df_pilares.columns:\n",
        "        momentum_and[p] = df_cambio_pilares.loc[ultimo_q, col]\n",
        "\n",
        "# Convertir a DataFrame para visualización\n",
        "df_momentum = pd.DataFrame(list(momentum_and.items()), columns=['Concepto', 'Cambio'])\n",
        "df_momentum['Tipo'] = ['IPA27'] + ['Dominio']*len(dominios_n) + ['Pilar']*len([p for p in pilares_n if f\"{p}_AND\" in df_pilares.columns])\n",
        "\n",
        "# Visualización\n",
        "fig, ax = plt.subplots(figsize=(14, 12))\n",
        "colors = ['#2E2925' if t == 'IPA27' else '#007932' if t == 'Dominio' else '#A8DADC' for t in df_momentum['Tipo']]\n",
        "sns.barplot(data=df_momentum, x='Cambio', y='Concepto', palette=colors, ax=ax)\n",
        "\n",
        "ax.set_title(f'Momentum IPA27: Variación Trimestral en puntos ({penultimo_q} -> {ultimo_q})\\\\n(Andalucía)', \n",
        "             fontsize=14, fontweight='bold', pad=20)\n",
        "ax.axvline(0, color='black', linewidth=1.5, linestyle='-')\n",
        "ax.grid(axis='x', alpha=0.3)\n",
        "\n",
        "# Etiquetas de valor\n",
        "for i, v in enumerate(df_momentum['Cambio']):\n",
        "    ax.text(v + (0.05 if v >= 0 else -0.2), i, f\"{v:+.2f}\", \n",
        "            va='center', fontweight='bold', fontsize=10, \n",
        "            color='#1e7e34' if v > 0 else '#bd2130' if v < 0 else 'black')\n",
        "\n",
        "plt.tight_layout()\n",
        "plt.savefig('results/figures/analysis/ipa27_momentum_trimestral.png', dpi=150, bbox_inches='tight', facecolor='white')\n",
        "plt.show()\n",
        "\n",
        "print(f\"✓ Gráfico de momentum guardado: results/figures/analysis/ipa27_momentum_trimestral.png\")"
    ]
}

try:
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # 1. Update export logic in Cell 35 (or similar)
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = cell['source']
            text = "".join(source)
            if 'def export_dashboard_data' in text:
                # Add momentum_global
                if '"global": round(df_hist.loc[last_q, \'IPA27_AND\'], 1)' in text:
                    for i, line in enumerate(source):
                        if '"global": round(df_hist.loc[last_q, \'IPA27_AND\'], 1)' in line:
                            source[i] = line.replace('\n', '') + ',\n'
                            source.insert(i+1, "            \"momentum_global\": round(df_ipa27.diff().loc[last_q, 'IPA27_AND'], 2),\n")
                            break
                
                # Add momentum_dominios
                if '"dominios": {d: round(df_dominios.loc[last_q, f\'{d}_AND\'], 1) for d in estructura.keys()}' in text:
                    for i, line in enumerate(source):
                        if '"dominios": {d: round(df_dominios.loc[last_q, f\'{d}_AND\'], 1) for d in estructura.keys()}' in line:
                            source[i] = line.replace('\n', '') + ',\n'
                            source.insert(i+1, "            \"momentum_dominios\": {d: round(df_dominios.diff().loc[last_q, f'{d}_AND'], 2) for d in estructura.keys()},\n")
                            break
                
                # Add momentum_pilares
                if '"pilares": {p: round(df_pilares.loc[last_q, f\'{p}_AND\'], 1) for d in estructura.values() for p in d.keys()}' in text:
                    for i, line in enumerate(source):
                        if '"pilares": {p: round(df_pilares.loc[last_q, f\'{p}_AND\'], 1) for d in estructura.values() for p in d.keys()}' in line:
                            source[i] = line.replace('\n', '') + ',\n'
                            # Get all pillar names from keys of all domain dicts
                            source.insert(i+1, "            \"momentum_pilares\": {p: round(df_pilares.diff().loc[last_q, f'{p}_AND'], 2) for d in estructura.values() for p in d.keys() if f'{p}_AND' in df_pilares.columns},\n")
                            break

    # 2. Insert the new analysis cell
    target_idx = -1
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown' and '# Exportación a dashboard' in "".join(cell['source']):
            target_idx = i
            break
    
    if target_idx != -1:
        # Check if already inserted to avoid duplicates
        found = False
        for j in range(max(0, target_idx-5), target_idx):
            if '# Análisis de Momentum' in "".join(nb['cells'][j]['source']):
                found = True
                break
        if not found:
            nb['cells'].insert(target_idx, NEW_ANALYSIS_CELL)
            nb['cells'].insert(target_idx, {"cell_type": "markdown", "metadata": {}, "source": ["# Análisis de Momentum\n"]})
            print("Inserted momentum analysis cell.")
    else:
        nb['cells'].append({"cell_type": "markdown", "metadata": {}, "source": ["# Análisis de Momentum\n"]})
        nb['cells'].append(NEW_ANALYSIS_CELL)
        print("Appended momentum analysis cell to end.")

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    
    print("Notebook updated successfully.")

except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
