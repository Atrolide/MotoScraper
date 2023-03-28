import requests
from bs4 import BeautifulSoup

url = 'https://www.otomoto.pl/oferta/volkswagen-golf-salon-pl-raport-autodna-oryginalny-przebieg-2-komplety-kol-ID6Fp0pp.html'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

elements_div = soup.find('div', {'class': 'offer-params with-vin'})

for ul in elements_div.find_all('ul', {'class': 'offer-params__list'}):
    for li in ul.find_all('li', {'class': 'offer-params__item'}):
        value_div = li.find('div', {'class': 'offer-params__value'})
        value_a = value_div.find('a', {'class': 'offer-params__link'})
        value = value_a.text.strip()
        print(value)

