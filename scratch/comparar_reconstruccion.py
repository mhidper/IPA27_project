import pandas as pd
import numpy as np

def comparar_ficheros():
    f_nuevo = r"G:\Mi unidad\Proyectos\IPA27_project\data\raw\cgpj_corrupcion_procesado.csv"
    f_viejo = r"G:\Mi unidad\Proyectos\IPA27_project\data\raw\cgpj_corrupcion_procesado - copia.csv"
    
    df_n = pd.read_csv(f_nuevo)
    df_v = pd.read_csv(f_viejo)
    
    # Asegurar tipos y orden
    for df in [df_n, df_v]:
        df['fecha'] = pd.to_datetime(df['fecha'])
        
    df_v = df_v.sort_values(['fecha', 'region'])
    df_n = df_n.sort_values(['fecha', 'region'])

    # Solo comparar hasta 2025-Q3 (ignorar Q4 si existe en el viejo)
    df_v_filt = df_v[df_v['Periodo'] != '2025-Q4'].copy()
    df_n_filt = df_n[df_n['Periodo'] != '2025-Q4'].copy()
    
    print(f"Registros en el nuevo: {len(df_n_filt)}")
    print(f"Registros en el viejo: {len(df_v_filt)}")
    
    # Alinear por indice
    df_v_filt = df_v_filt.set_index(['fecha', 'region']).sort_index()
    df_n_filt = df_n_filt.set_index(['fecha', 'region']).sort_index()
    
    # Seleccionar solo columnas numericas
    cols_num = ['procedimientos_corrupcion', 'procedimientos_ingresados', 'procedimientos_resueltos', 'GOB_EFF', 'GOB_COR']
    
    # Diferencias
    diff = (df_n_filt[cols_num] - df_v_filt[cols_num]).abs().round(4)
    total_diff = diff.sum().sum()
    
    if total_diff == 0 and len(df_n_filt) == len(df_v_filt):
        print("\nIDENTICOS: Los datos reconstruidos coinciden al 100% con el original hasta 2025-Q3.")
    else:
        print(f"\nAVISO: Hay diferencias o falta de registros.")
        print(f"Suma de diferencias: {total_diff}")
        if len(df_n_filt) != len(df_v_filt):
            print(f"Diferencia en numero de filas: {len(df_n_filt)} vs {len(df_v_filt)}")
        
        # Localizar el primer error
        error_mask = (diff > 0).any(axis=1)
        if error_mask.any():
            print("\nEjemplo de discrepancia:")
            print("NUEVO:")
            print(df_n_filt[error_mask].head(1))
            print("VIEJO:")
            print(df_v_filt[error_mask].head(1))

if __name__ == "__main__":
    comparar_ficheros()
