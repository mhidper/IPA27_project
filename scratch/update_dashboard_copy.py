import json
import os
import shutil

def update_02_3_dashboard_sync():
    nb_path = r"g:\Mi unidad\Proyectos\IPA27_project\notebooks\02_3_exportacion_geometricas.ipynb"
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    for i, cell in enumerate(nb['cells']):
        if cell.get('cell_type') == 'code':
            src = "".join(cell['source'])
            if "def export_dashboard_data" in src:
                src_replaced = src.replace(
                    "print(f\"✅ Datos exportados exitosamente a {output_path}\")",
                    "root_json = os.path.join('results', 'data', 'dashboard_data.json')\n    with open(root_json, 'w', encoding='utf-8') as f:\n        json.dump(dashboard_json, f, ensure_ascii=False, indent=2)\n    print(f\"✅ Datos exportados exitosamente a {output_path} y sincronizados en {root_json}\")"
                ).replace(
                    "print(f\"✅ Series finales exportadas exitosamente a Excel en: {excel_path}\")",
                    "root_excel = os.path.join('results', 'data', 'IPA27_series_finales.xlsx')\n        df_excel.to_excel(root_excel)\n        print(f\"✅ Series finales exportadas exitosamente a Excel en: {excel_path} y {root_excel}\")"
                )
                cell['source'] = [line + '\n' for line in src_replaced.split('\n') if line]
                print(f"Updated export_dashboard_data sync in cell {i}")

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

    # Sync today's files right now
    today_dir = r"g:\Mi unidad\Proyectos\IPA27_project\results\data\data20260904"
    if os.path.exists(today_dir):
        json_src = os.path.join(today_dir, "dashboard_data.json")
        json_dst = r"g:\Mi unidad\Proyectos\IPA27_project\results\data\dashboard_data.json"
        if os.path.exists(json_src):
            shutil.copy2(json_src, json_dst)
            print(f"Synced {json_src} -> {json_dst}")

if __name__ == '__main__':
    update_02_3_dashboard_sync()
    print("DASHBOARD SYNC UPDATED SUCCESSFULLY.")
