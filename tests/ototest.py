import requests
from bs4 import BeautifulSoup

# Set MAXHEADERS to 1000 to get rid of HTTP Exception error
import http.client

http.client._MAXHEADERS = 1000

url = 'https://www.otomoto.pl/oferta/ford-f150-ford-f150-ID6FpibS.html'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Parent div
parent_div = soup.find('div', {'class': 'flex-container-main'})

# Successive access to `div` tags
child1_div = parent_div.find('div', {'class': 'flex-container-main__left'})
child2_div = child1_div.find('div', {'class': 'offer-content offer-content--secondary'})
child3_div = child2_div.find('div', {'class': 'offer-content__row om-offer-main'})
child4_div = child3_div.find('div', {'class': 'offer-content__main-column'})
child5_div = child4_div.find('div', {'class': 'parametersArea'})
child6_div = child5_div.find('div', {'class': 'offer-params with-vin'})

# Access to `ul` tag
child7_ul = child6_div.find('ul', {'class': 'offer-params__list'})

# Access to `li` tags
child8_li = child7_ul.find_all('li', {'class': 'offer-params__item'})

brand = ''
model = ''
version = ''
year = ''
mileage = ''
engine_size = ''
fuel_type = ''
horse_power = ''

for child in range(0, len(child8_li)):
    if child8_li[child].find('span', {'class': 'offer-params__label'}).text.strip() == 'Marka pojazdu':
        brand = child8_li[child].find('div', {'class': 'offer-params__value'}).text.strip()

    if child8_li[child].find('span', {'class': 'offer-params__label'}).text.strip() == 'Model pojazdu':
        model = child8_li[child].find('div', {'class': 'offer-params__value'}).text.strip()

    if child8_li[child].find('span', {'class': 'offer-params__label'}).text.strip() == 'Wersja':
        version = child8_li[child].find('div', {'class': 'offer-params__value'}).text.strip()

    if child8_li[child].find('span', {'class': 'offer-params__label'}).text.strip() == 'Rok produkcji':
        year = child8_li[child].find('div', {'class': 'offer-params__value'}).text.strip()

    if child8_li[child].find('span', {'class': 'offer-params__label'}).text.strip() == 'Przebieg':
        mileage = child8_li[child].find('div', {'class': 'offer-params__value'}).text.strip()

    if child8_li[child].find('span', {'class': 'offer-params__label'}).text.strip() == 'Pojemność skokowa':
        engine_size = child8_li[child].find('div', {'class': 'offer-params__value'}).text.strip()

    if child8_li[child].find('span', {'class': 'offer-params__label'}).text.strip() == 'Rodzaj paliwa':
        fuel_type = child8_li[child].find('div', {'class': 'offer-params__value'}).text.strip()

    if child8_li[child].find('span', {'class': 'offer-params__label'}).text.strip() == 'Moc':
        horse_power = child8_li[child].find('div', {'class': 'offer-params__value'}).text.strip()

print(brand, model, version, year, mileage, engine_size, fuel_type, horse_power)

