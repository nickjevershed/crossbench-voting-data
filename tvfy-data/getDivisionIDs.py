#%%
import requests
import scraperwiki
import os
from datetime import datetime, timedelta
import time

API_KEY = os.environ['TVFY_API']

# Start from the date the 47th parliament opened
start_date = '2025-02-01'

# Convert start_date string to datetime object
current_date = datetime.strptime(start_date, '%Y-%m-%d')
today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)


def saveData(data):
    scraperwiki.sqlite.save(unique_keys=["id"], data=data, table_name="divisions")
    # for row in data:
    #     print(row)
        
  

# Test the saveData function

# url = f'https://theyvoteforyou.org.au/api/v1/divisions.json?key={API_KEY}&house=representatives&start_date=2022-07-26&end_date=2022-08-07'
# response = requests.get(url)
# data = response.json()
# saveData(data)

# # Loop through dates in weekly increments until reaching today
while current_date <= today:
    # Set the end date to one week after current date
    end_date = (current_date + timedelta(days=7)).strftime('%Y-%m-%d')
    
    # If end_date would be in the future, cap it at today
    if datetime.strptime(end_date, '%Y-%m-%d') > today:
        end_date = today.strftime('%Y-%m-%d')
    
    print(f"Processing from {current_date.strftime('%Y-%m-%d')} to {end_date}")
    
    # Here you can add your API call logic using current_date.strftime('%Y-%m-%d') and end_date
    url = f'https://theyvoteforyou.org.au/api/v1/divisions.json?key={API_KEY}&house=representatives&start_date={current_date.strftime("%Y-%m-%d")}&end_date={end_date}'
    print("Getting", url)
    response = requests.get(url)
    data = response.json()
    saveData(data)
    time.sleep(1)
    # Move to the next date range
    current_date = current_date + timedelta(days=7)

