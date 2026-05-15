import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = "https://www.juntadeandalucia.es/institutodeestadisticaycartografia/intranet/admin/rest/v1.0"
consulta_id = "106166"

meta = requests.get(f"{base_url}/consulta/{consulta_id}", verify=False).json()
temp_hier = next(h for h in meta['hierarchies'] if h['alias'] == 'D_TEMPORAL_0')
jer_data = requests.get(temp_hier['url'], verify=False).json()

ids = []
def extract_ids(item):
    if item.get('levelId') == 3:
        cod = str(item.get('cod', ''))
        if len(cod) == 5: ids.append(str(item['id']))
    children = item.get('children', [])
    if children:
        for child in children: extract_ids(child)

extract_ids(jer_data.get('data', {}))
ids_str = ",".join(ids)

url = f"{base_url}/consulta/{consulta_id}?D_CRTA_COMPONPIB2008_0=69618&D_TEMPORAL_0={ids_str}"
print(f"URL length: {len(url)}")

res = requests.get(url, verify=False).json()
print(f"Data records returned: {len(res.get('data', []))}")

found_20261 = False
for item in res.get('data', []):
    if item[1]['cod'][0] == '20261':
        found_20261 = True
        print(f"FOUND 20261: {item[4].get('val')}")
        break

if not found_20261:
    print("20261 NOT found in data response!")
