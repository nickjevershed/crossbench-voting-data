#%%
import requests
import json
import csv
import os
#%%
# Saves 600 divisions in date range for the 47th parliament to a json file

url = "https://divisions.aph.gov.au/api/division?f=2022-7-26&t=2025-3-20&page=0&ps=600&_=1742442671245"

with open('original_divisions.json', 'w') as f:
    response = requests.get(url)
    data = response.json()
    json.dump(data, f, indent=4)

#%% Make politicians CSV into a kay-value dictionary
# Note that there are some politicians who changed party, Andrew Gee and Russel Broadbent, they
# will be in here as Independent rather than Liberal Party

with open("politicians.csv", mode="r") as file:
    reader = csv.DictReader(file)
    politicians = {row["Name"]: row["Party"] for row in reader}

#%%
with open('original_divisions.json','r') as f:
    divisions_json = json.load(f)

new_data = []

for division in divisions_json['results']:
    division['mover'] = division['mover']['name']
    if division['mover'] != "":
        division['mover_party'] = politicians[division['mover']]
    new_data.append(division)

with open('formatted_divisions.json', 'w') as f:
    json.dump(new_data, f, indent=4)
    