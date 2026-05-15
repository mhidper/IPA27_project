import pandas as pd
import matplotlib.pyplot as plt

def plot_comparativa():
    f_nuevo = r"G:\Mi unidad\Proyectos\IPA27_project\data\raw\cgpj_corrupcion_procesado.csv"
    f_viejo = r"G:\Mi unidad\Proyectos\IPA27_project\data\raw\cgpj_corrupcion_procesado - copia.csv"
    
    df_n = pd.read_csv(f_nuevo)
    df_v = pd.read_csv(f_viejo)
    
    # Filtrar Andalucia y convertir fechas
    df_n = df_n[df_n['region'] == 'AND'].copy()
    df_v = df_v[df_v['region'] == 'AND'].copy()
    
    df_n['fecha'] = pd.to_datetime(df_n['fecha'])
    df_v['fecha'] = pd.to_datetime(df_v['fecha'])
    
    df_n = df_n.sort_values('fecha')
    df_v = df_v.sort_values('fecha')

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    
    # Grafico Corrupcion (GOB_COR)
    ax1.plot(df_v['fecha'], df_v['GOB_COR'], 'o-', label='Original (Copia)', color='blue', alpha=0.6)
    ax1.plot(df_n['fecha'], df_n['GOB_COR'], 'x--', label='Reconstruido (Nuevo)', color='red', alpha=0.8)
    ax1.set_title('Comparativa GOB_COR (Corrupción) - Andalucía')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # Grafico Eficiencia (GOB_EFF)
    ax2.plot(df_v['fecha'], df_v['GOB_EFF'], 'o-', label='Original (Copia)', color='green', alpha=0.6)
    ax2.plot(df_n['fecha'], df_n['GOB_EFF'], 'x--', label='Reconstruido (Nuevo)', color='orange', alpha=0.8)
    ax2.set_title('Comparativa GOB_EFF (Eficiencia) - Andalucía')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    output_plot = r"G:\Mi unidad\Proyectos\IPA27_project\scratch\comparativa_andalucia.png"
    plt.savefig(output_plot)
    print(f"Grafico guardado en: {output_plot}")

if __name__ == "__main__":
    plot_comparativa()
