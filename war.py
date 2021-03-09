from bs4 import BeautifulSoup
import requests

base_url = 'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=6&season=2019&month=0&season1=2019&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate=2019-01-01&enddate=2019-12-31&'
ends = ['page=1_50','page=2_50', 'page=3_50']

d = {}
for end in ends:
    url = base_url + end
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    all_tr = soup.find_all('tr', {'class': ['rgRow', 'rgAltRow']})
    #print(all_tr)
    for tr in all_tr:
        tags = tr.find_all('td', class_='grid_line_regular')
        tag = tags[1].find('a')
        name = tag.text
        link = tag.get('href')
        war = tags[9].text
        d[name] = [war, link]

print(d)