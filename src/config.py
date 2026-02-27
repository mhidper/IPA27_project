import os

# Base Directory Setup
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW = os.path.join(BASE_PATH, 'data', 'raw')
DATA_PROCESSED = os.path.join(BASE_PATH, 'data', 'processed')
GRAFICOS = os.path.join(BASE_PATH, 'graficos')

# Create directories
for d in [DATA_RAW, DATA_PROCESSED, GRAFICOS]:
    os.makedirs(d, exist_ok=True)

# Common Constants
REGIONS = {
    'ESP': 'España',
    'AND': 'Andalucía',
    'ARA': 'Aragón',
    'AST': 'Principado de Asturias',
    'BAL': 'Illes Balears',
    'CAN': 'Canarias',
    'CANT': 'Cantabria',
    'CASTL': 'Castilla y León',
    'CASTM': 'Castilla-La Mancha',
    'CAT': 'Cataluña',
    'VAL': 'Comunitat Valenciana',
    'EXT': 'Extremadura',
    'GAL': 'Galicia',
    'MAD': 'Comunidad de Madrid',
    'MUR': 'Región de Murcia',
    'NAV': 'Comunidad Foral de Navarra',
    'PVA': 'País Vasco',
    'RIO': 'La Rioja',
    'CEU': 'Ceuta',
    'MEL': 'Melilla'
}

FREQUENCIES = {
    'M': 'Mensual',
    'Q': 'Trimestral',
    'A': 'Anual'
}
