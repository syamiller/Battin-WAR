from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import json

base_url = 'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=6&season=2019&month=0&season1=2019&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate=2019-01-01&enddate=2019-12-31&'
ends = ['page=1_50','page=2_50', 'page=3_50']

d = {}
for end in ends:
    url = base_url + end
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    all_tr = soup.find_all('tr', {'class': ['rgRow', 'rgAltRow']})
    for tr in all_tr:
        tags = tr.find_all('td', class_='grid_line_regular')
        tag = tags[1].find('a')
        name = tag.text
        war = tags[9].text
        d[name] = float(war)

l = []
url = 'https://www.usatoday.com/sports/mlb/salaries/2019/player/all/'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
table = soup.find('tbody')
trs = table.find_all('tr')
for tr in trs:
    tag = tr.find('div', class_='sp-details-open')
    name = tag.text.strip()
    if name in d.keys():
        tag = tr.find('td', class_='salary')
        salary = tag.text.strip()
        salary = salary.replace('$', '')
        salary = salary.replace(',', '')
        l.append({'WAR': d.get(name, None), 'Salary': float(salary)})

frame = {}
frame['frame'] = l
with open('wardata.json', 'w') as f:
    json.dump(frame, f)

df = pd.DataFrame(frame['frame'])
df.plot.scatter(x='WAR', y='Salary')
plt.show()