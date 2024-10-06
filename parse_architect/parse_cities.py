from bs4 import BeautifulSoup

soup = BeautifulSoup(open('cities.html', encoding='utf-8'), 'html.parser')

cities = []
for li in soup.find_all('li'):
    cities.append(li.find('a').get('ui_val'))

print(cities.index('ustyuzhna'))