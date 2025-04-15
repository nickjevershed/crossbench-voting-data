#%%
import requests 
import json

#%%
with open('formatted_divisions.json','r') as f:
    divisions = json.load(f)

for division in divisions:
        with open(f"division_data_json/{division['divisionId']}.json",'r') as f:
            division_info = json.load(f)
            division['division_type'] = ""
            if len(division_info['bills']) > 0:
                division['bill_id'] = division_info['bills'][0]['parlinfoBillId']
                division['bill_title'] = division_info['bills'][0]['title']
                division['division_type'] = "bill"
            else: 
                division['division_type'] = "procedural"

        print(division)


with open('formatted_divisions.json', 'w') as f:
    json.dump(divisions, f, indent=4)