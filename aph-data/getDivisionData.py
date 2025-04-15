#%%
import json
import pandas
import os
#%%
# test_url = "https://divisions.aph.gov.au/api/division/2421/report/csv"

# df = pandas.read_csv(test_url, skiprows=12)

# Check files we already have

files = os.listdir('division_data_csv')
files = [x.split(".csv")[0] for x in files ]

#%%

with open('formatted_divisions.json','r') as f:
    divisions_json = json.load(f)

for division in divisions_json:
    if str(division['divisionId']) not in files:
        url = f"https://divisions.aph.gov.au/api/division/{division['divisionId']}/report/csv"
        print("Getting", url)
        temp_df = pandas.read_csv(url, skiprows=12)
        temp_df.to_csv(f"division_data_csv/{division['divisionId']}.csv")


#%%
import requests
with open('formatted_divisions.json','r') as f:
    divisions_json = json.load(f)

for division in divisions_json:
    url = f"https://divisions.aph.gov.au/api/division/{division['divisionId']}"
    print("Getting", url)
    r = requests.get(url)
    with open(f'division_data_json/{division["divisionId"]}.json', 'w') as f:
        json.dump(r.json(), f, indent=4)


