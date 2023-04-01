import requests
from bs4 import BeautifulSoup

url = 'https://www.otomoto.pl/osobowe'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

car_links = []

for link in soup.find_all('a', {'class': 'offer-title__link'}):
    car_links.append(link.get('href'))

print(car_links)
