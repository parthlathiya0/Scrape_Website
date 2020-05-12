from time import sleep
from bs4 import BeautifulSoup
import requests

pages = [
    'https://www.allsides.com/media-bias/media-bias-ratings',
    'https://www.allsides.com/media-bias/media-bias-ratings?page=1'
]

# derived this logic from the javascript of the webpage
def get_agreeance_text(ratio):
    if ratio > 3: return                "absolutely agrees"
    elif 2 < ratio <= 3: return         "strongly agrees"
    elif 1.5 < ratio <= 2: return       "agrees"
    elif 1 < ratio <= 1.5: return       "somewhat agrees"
    elif ratio == 1: return             "neutral"
    elif 0.67 < ratio < 1: return       "somewhat disagrees"
    elif 0.5 < ratio <= 0.67: return    "disagrees"
    elif 0.33 < ratio <= 0.5: return    "strongly disagrees"
    elif ratio <= 0.33: return          "absolutely disagrees"
    else: return None


''' 
According to AllSides' robots.txt[https://www.allsides.com/robots.txt] we need to make sure we wait ten seconds before each request.Our loop will:
    - request a page
    - parse the page
    - wait ten seconds
    - repeat for next page. 
'''

all_data= []
for index, page in enumerate(pages):
    
    print("\n\nIteration : ",index)
    r = requests.get(page)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    rows = soup.select('tbody tr')
    for row in rows:
        d = dict()
        d['name'] = row.select_one('.source-title').text.strip()
        d['allsides_page'] = 'https://www.allsides.com' + row.select_one('.source-title a')['href']
        d['bias'] = row.select_one('.views-field-field-bias-image a')['href'].split('/')[-1]
        d['agree'] = int(row.select_one('.agree').text)
        d['disagree'] = int(row.select_one('.disagree').text)
        d['agree_ratio'] = d['agree'] / d['disagree']
        d['agreeance_text'] = get_agreeance_text(d['agree_ratio'])

        all_data.append(d)
    sleep(10)           

print("\nAll data length :", len(all_data))

# $Store and retrive data to/from local disk file
import json
with open('allsides.json', 'w') as f:
    json.dump(all_data, f)

with open('allsides.json', 'r') as f:
    data = json.load(f)