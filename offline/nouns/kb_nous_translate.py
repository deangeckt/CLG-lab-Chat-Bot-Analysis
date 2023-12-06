"""
This script should run under the Server repo - KB files are there
"""
import json
from google_cloud.translate import Translate
import pandas as pd
translate = Translate()



i =1
names = []

kb_path = f'map_{i+1}.json'
with open(kb_path, 'r') as f:
    kb = json.load(f)

    for obj in kb['absolute']:
        names.append(obj)
        if 'synonym' in kb['absolute'][obj]:
            names.extend(kb['absolute'][obj]['synonym'])

# print(names)

es_names =  [translate.translate_to_spa(n) for n in names]
data = {'eng': names, 'es': es_names}
df = pd.DataFrame(data)
df.to_csv(f'map_{i+1}_names.csv')
