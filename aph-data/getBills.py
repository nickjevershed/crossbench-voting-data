#%%
import requests
import lxml.html
import json
import re

with open('formatted_divisions.json','r') as f:
    divisions = json.load(f)

def remove_non_alpha(s):
    return re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$', '', s)

def split_at_first_alnum(s):
    match = re.search(r'\w', s)  # Find first alphanumeric character
    if match:
        index = match.start()
        return s[:index], s[index:]
    return s, ''

for division in divisions:    
    if division['division_type'] == 'bill':

        url = f"https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/Bills_Search_Results/Result?bId={division['bill_id']}"
        print("Getting", url)
        r = requests.get(url)
        dom = lxml.html.fromstring(r.content)
        summary_div = dom.cssselect('#main_0_billSummary_divHeader')[0]
        if "Previous Citations" in summary_div.text_content():
            bill_type = summary_div.cssselect('.dl--inline--bills dd')[1].text
            portfolio = summary_div.cssselect('.dl--inline--bills dd')[2].text
            orig_house = summary_div.cssselect('.dl--inline--bills dd')[3].text
            status = summary_div.cssselect('.dl--inline--bills dd')[4].text
        else:    
            bill_type = summary_div.cssselect('.dl--inline--bills dd')[0].text
            portfolio = summary_div.cssselect('.dl--inline--bills dd')[1].text
            orig_house = summary_div.cssselect('.dl--inline--bills dd')[2].text
            status = summary_div.cssselect('.dl--inline--bills dd')[3].text

        division['bill_type'] = remove_non_alpha(bill_type)
        division['portfolio'] = remove_non_alpha(portfolio)
        division['orig_house'] = remove_non_alpha(orig_house)
        division['status'] = remove_non_alpha(status)

        summary = dom.cssselect('#main_0_summaryPanel p')[0].text_content().strip()
        division['summary'] = summary

with open('formatted_divisions.json', 'w') as f:
    json.dump(divisions, f, indent=4)