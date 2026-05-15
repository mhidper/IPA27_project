import os
import glob
import requests
import re

def get_next_period(directory):
    files = glob.glob(os.path.join(directory, "cgpj_*.html"))
    if not files:
        return 2016, 1
    
    max_anio = 0
    max_trim = 0
    
    for f in files:
        match = re.search(r'cgpj_(\d{4})_Q(\d)', os.path.basename(f))
        if match:
            anio, trim = map(int, match.groups())
            if anio > max_anio or (anio == max_anio and trim > max_trim):
                max_anio = anio
                max_trim = trim
    
    # Calcular el siguiente
    if max_trim == 4:
        return max_anio + 1, 1
    else:
        return max_anio, max_trim + 1

def download_cgpj(anio, trim, output_path):
    # URL para ambito Comunidades Autonomas (comunidad=00 suele ser el desglosado)
    url = f"https://www.poderjudicial.es/cgpj/es/Temas/Transparencia/Repositorio-de-datos-sobre-procesos-por-corrupcion/ch.Consulta-de-datos.formato2/?comunidad=00&anio={anio}&trimestre={trim}"
    
    print(f"Intentando descargar: {anio}-Q{trim} desde {url}")
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            content = response.text
            # Verificar si hay tablas con datos (buscamos la etiqueta <table>)
            if "<table" in content.lower():
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Exito: Archivo guardado en {output_path}")
                return True
            else:
                print(f"Aviso: La pagina cargo pero no parece tener tablas de datos para {anio}-Q{trim}.")
                return False
        else:
            print(f"Error: La web respondio con codigo {response.status_code}")
            return False
    except Exception as e:
        print(f"Error en la conexion: {e}")
        return False

if __name__ == "__main__":
    raw_dir = r"G:\Mi unidad\Proyectos\IPA27_project\data\raw\cgpj"
    next_anio, next_trim = get_next_period(raw_dir)
    print(f"Ultimo periodo detectado. El siguiente a buscar es: {next_anio}-Q{next_trim}")
    
    filename = f"cgpj_{next_anio}_Q{next_trim}.html"
    target_path = os.path.join(raw_dir, filename)
    
    download_cgpj(next_anio, next_trim, target_path)
