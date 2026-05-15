import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

def plot_corruption():
    csv_path = r"G:\Mi unidad\Proyectos\IPA27_project\data\raw\cgpj_corrupcion_procesado.csv"
    df = pd.read_csv(csv_path)
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    plt.figure(figsize=(12, 6))
    
    # Filtrar por Andalucia y España
    for region, label, color in [('AND', 'Andalucia', '#e74c3c'), ('ESP', 'España (Total)', '#2c3e50')]:
        sub = df[df['region'] == region].sort_values('fecha')
        plt.plot(sub['fecha'], sub['GOB_COR'], marker='o', label=label, color=color, linewidth=2, markersize=4)
        
        # Anotar el ultimo punto (2025-Q4)
        last_row = sub.iloc[-1]
        plt.annotate(f"{int(last_row['GOB_COR'])}", 
                     (last_row['fecha'], last_row['GOB_COR']),
                     textcoords="offset points", xytext=(0,10), ha='center',
                     fontsize=10, fontweight='bold', color=color)

    plt.title('Evolucion de Procedimientos por Corrupcion (CGPJ)', fontsize=14, fontweight='bold')
    plt.ylabel('Numero de Procedimientos / Acusados', fontsize=12)
    plt.xlabel('Fecha (Trimestres)', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Formato de fechas
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    
    plt.tight_layout()
    output_img = r"G:\Mi unidad\Proyectos\IPA27_project\scratch\grafico_corrupcion_final.png"
    plt.savefig(output_img)
    print(f"Grafico guardado en: {output_img}")

if __name__ == "__main__":
    plot_corruption()
