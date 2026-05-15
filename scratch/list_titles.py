from bs4 import BeautifulSoup

def list_table_titles(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    for i, table in enumerate(soup.find_all('table')):
        # Buscar el texto que precede a la tabla (h2, h3, p o un div con clase titulo)
        prev = table.find_previous(['h1', 'h2', 'h3', 'p', 'strong', 'div'])
        title = prev.text.strip() if prev else "Sin título"
        print(f"T{i}: {title}")

if __name__ == "__main__":
    list_table_titles(r"G:\Mi unidad\Proyectos\IPA27_project\data\raw\cgpj\cgpj_2016_Q1.html")
