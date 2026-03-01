import json
import pandas as pd

# Load the current json
with open('G:/Mi unidad/Proyectos/IPA27_project/dashboard/public/data/dashboard_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# The labels from the evolution
labels = data['evolution']['labels']

# Read the dominios CSV
df_dominios = pd.read_csv('G:/Mi unidad/Proyectos/IPA27_project/results/data/contribuciones_dominios_ipa27.csv')

# Map to array
dominios = ['Sociedades Inclusivas', 'Economías Abiertas', 'Personas Empoderadas']
and_dominios = {}
for dom in dominios:
    # Handle the accent in Economías Abiertas
    if dom == 'Economías Abiertas':
        # the csv might have a mojibake for Economías depending on encoding. Let's do a contains 'Abiertas'
        df_d = df_dominios[df_dominios['Dominio'].str.contains('Abiertas')]
    else:
        df_d = df_dominios[df_dominios['Dominio'] == dom]
        
    vals = []
    for label in labels:
        row = df_d[df_d['Periodo'] == label]
        if not row.empty:
            vals.append(round(float(row.iloc[0]['Score']), 2))
        else:
            vals.append(None)
    and_dominios[dom] = vals

# Inject into json
data['evolution']['and_dominios'] = and_dominios

# Save
with open('G:/Mi unidad/Proyectos/IPA27_project/dashboard/public/data/dashboard_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Injected and_dominios into dashboard_data.json")
