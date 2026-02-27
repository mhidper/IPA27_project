import json
import pandas as pd
import os

def export_dashboard_data(df_global, df_dominios, df_pilares, df_norm, estructura, output_path):
    """
    Simula la lógica que debería ir en el notebook para generar el JSON.
    """
    # 1. Definir nombres amigables para los indicadores
    INDICADORES_NOMBRES = {
        'SEG_BAL': 'Balance de Criminalidad',
        'SEG_CRI': 'Tasa de Delitos',
        'LIB_ODI': 'Delitos de Odio',
        'LIB_SEX': 'Violencia Género',
        'GOB_DES': 'Desempleo (Pilar Gob.)',
        'GOB_EFF': 'Eficacia Institucional',
        'SOC_ASO': 'Asociacionismo',
        'SOC_PAR_enlazado': 'Participación Electoral',
        'INV_HIP': 'Hipotecas',
        'INV_IED': 'Inversión Extranjera',
        'EMP_NAT': 'Nacimientos Empresas',
        'EMP_SOC': 'Sociedades Mercantiles',
        'INF_BAN': 'Bancarización',
        'INF_TRA': 'Tráfico Ferroviario',
        'ECO_RBHpc': 'Renta Bruta Habitante',
        'ECO_COL_sal': 'Coste Salarial Real',
        'VID_ARO': 'Tasa AROPE',
        'VID_PAR': 'Paro Larga Duración',
        'SAL_ESP': 'Esperanza de Vida',
        'SAL_SAT_enlazado': 'Satisfacción Sanitaria',
        'EDU_ABA': 'Abandono Escolar',
        'EDU_SUP': 'Educación Superior',
        'CON_IDI': 'Inversión I+D',
        'CON_OCI': 'Ocupación Conocimiento'
    }

    # 2. Preparar históricos (2015-2025)
    # df_global tiene índice Period
    df_hist = df_global.loc['2015Q1':].copy()
    evolution = {
        "labels": [str(p) for p in df_hist.index],
        "and_global": df_hist['IPA27_AND'].round(2).tolist(),
        "esp_global": df_hist['IPA27_ESP'].round(2).tolist()
    }

    # 3. Datos último trimestre
    last_q = df_hist.index[-1]
    
    current_data = {
        "periodo": str(last_q),
        "and": {
            "global": round(df_hist.loc[last_q, 'IPA27_AND'], 1),
            "dominios": {d: round(df_dominios.loc[last_q, f'{d}_AND'], 1) for d in estructura.keys()},
            "pilares": {p: round(df_pilares.loc[last_q, f'{p}_AND'], 1) for d in estructura.values() for p in d.keys()},
            "indicadores": {ind: round(df_norm.loc[last_q, f'{ind}_AND'], 1) for d in estructura.values() for p in d.values() for ind in p}
        },
        "esp": {
            "global": round(df_hist.loc[last_q, 'IPA27_ESP'], 1),
            "dominios": {d: round(df_dominios.loc[last_q, f'{d}_ESP'], 1) for d in estructura.keys()},
            "pilares": {p: round(df_pilares.loc[last_q, f'{p}_ESP'], 1) for d in estructura.values() for p in d.keys()},
        }
    }

    # 4. Cuellos de botella
    ind_and_vals = {ind: df_norm.loc[last_q, f'{ind}_AND'] for d in estructura.values() for p in d.values() for ind in p}
    sorted_inds = sorted(ind_and_vals.items(), key=lambda x: x[1])
    bottlenecks = [
        {"code": item[0], "name": INDICADORES_NOMBRES.get(item[0], item[0]), "value": round(item[1], 1)} 
        for item in sorted_inds[:3]
    ]

    # 5. Consolidar
    dashboard_json = {
        "metadata": {
            "last_update": str(last_q),
            "indicator_names": INDICADORES_NOMBRES,
            "structure": estructura
        },
        "evolution": evolution,
        "current": current_data,
        "bottlenecks": bottlenecks
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dashboard_json, f, ensure_ascii=False, indent=2)
    
    return f"✅ Exportado a {output_path}"

# Este script no se puede ejecutar directamente aquí por falta de los DataFrames en memoria de Python fuera del notebook, 
# pero servirá de base para la actualización de la web.
