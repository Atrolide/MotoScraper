import requests
from bs4 import BeautifulSoup

url_template = 'https://www.otomoto.pl/osobowe?page={}'

for page_num in range(1, 3):
    url = url_template.format(page_num)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    elements = soup.find_all('article', {'data-testid': 'listing-ad'})

    for element in elements:
        ad_title_link = element.find('h2', {'data-testid': 'ad-title'})
        ad_url = ad_title_link.a['href']

        response = requests.get(ad_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        parent_div = soup.find('div', {'class': 'flex-container-main'})

        final_child_div = parent_div.find('div', {'class': 'flex-container-main__left'}) \
            .find('div', {'class': 'offer-content offer-content--secondary'}) \
            .find('div', {'class': 'offer-content__row om-offer-main'}) \
            .find('div', {'class': 'offer-content__main-column'}) \
            .find('div', {'class': 'parametersArea'}) \
            .find('div', {'class': 'offer-params with-vin'})

        # ...

        child7_ul = None
        if final_child_div:
            child7_ul = final_child_div.find('ul', {'class': 'offer-params__list'})

        if child7_ul:
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
                label = child8_li[child].find('span', {'class': 'offer-params__label'}).text.strip()
                value = child8_li[child].find('div', {'class': 'offer-params__value'})
                if value:
                    value = value.text.strip()

                if label == 'Marka pojazdu':
                    brand = value if value else ''
                elif label == 'Model pojazdu':
                    model = value if value else ''
                elif label == 'Wersja':
                    version = value if value else ''
                elif label == 'Rok produkcji':
                    year = value if value else ''
                elif label == 'Przebieg':
                    mileage = value if value else ''
                elif label == 'Pojemność skokowa':
                    engine_size = value if value else ''
                elif label == 'Rodzaj paliwa':
                    fuel_type = value if value else ''
                elif label == 'Moc':
                    horse_power = value if value else ''

            print(brand, model, version, year, mileage, engine_size, fuel_type, horse_power)
