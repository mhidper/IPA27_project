import pandas as pd
import os

path = r'g:\Mi unidad\Proyectos\IPA27_project\results\data\ipa27_raw_20260510.xlsx'
df = pd.read_excel(path)
print("Columns:", df.columns.tolist())
print("Head:")
print(df.head())
print("Unique Regions:", df['region'].unique() if 'region' in df.columns else "No region col")
