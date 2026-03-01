import json

nb_path = 'G:/Mi unidad/Proyectos/IPA27_project/notebooks/02_procesamiento_IPA27_CCAA.ipynb'
try:
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # Let's insert a call to export_dashboard_data at the end of cell 35 if it's not there
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = cell['source']
            if "def export_dashboard_data" in "".join(source):
                if not "export_dashboard_data(" in "".join(source[-3:]):
                    cell['source'].append("\n# Llamada automática para actualizar JSON de la web\n")
                    cell['source'].append("print('Generando dashboard_data.json...')\n")
                    cell['source'].append("export_dashboard_data(df_ipa27_filtrado, df_dominios_filtrado, df_pilares_filtrado, df_norm_filtrado, ESTRUCTURA, '../dashboard/public/data/dashboard_data.json')\n")
                    print("Appended export_dashboard_data call.")

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
except Exception as e:
    print(e)
