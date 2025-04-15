import scraperwiki
import json
import os
import requests
import time

API_KEY = os.environ['TVFY_API']
divisions = scraperwiki.sqlite.select("* from divisions")

for division in divisions:
    url = f'https://theyvoteforyou.org.au/api/v1/divisions/{division["id"]}.json?key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    with open(f'division_data/{division["id"]}.json', 'w') as f:
        json.dump(data, f)
    time.sleep(1)    
