import requests
from bs4 import BeautifulSoup


def get_ad_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    elements = soup.find_all('article', {'data-testid': 'listing-ad'})

    links = [element.find('h2', {'data-testid': 'ad-title'}).a['href'] for element in elements]

    return links


def scrape_ad(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    parent_div = soup.find('div', {'class': 'flex-container-main'}) \
        .find('div', {'class': 'flex-container-main__left'})

    primary_child_div = parent_div.find('div', {'class': 'offer-content offer-content--primary'}) \
        .find('div', {'class': 'offer-content__row'}) \
        .find('div', {'class': 'flex-container'}) \
        .find('div', {'class': 'offer-header__row visible-xs'}) \
        .find('div', {'class': 'visible-mweb'}) \
        .find('div', {'class': 'offer-price changeFinanceLinkOrder'})

    secondary_child_div = parent_div.find('div', {'class': 'offer-content offer-content--secondary'}) \
        .find('div', {'class': 'offer-content__row om-offer-main'}) \
        .find('div', {'class': 'offer-content__main-column'}) \
        .find('div', {'class': 'parametersArea'}) \
        .find('div', {'class': 'offer-params with-vin'})

    photo_div = soup.find_all('div', {'class': 'photo-item'})
    photo_url = photo_div[0].find('img')['data-lazy'] if photo_div else None

    price = primary_child_div.find('span', {'class': 'offer-price__number'}).text.strip()
    word_to_remove = " PLN"
    price = price.replace(word_to_remove, "")
    price = price + "PLN"

    parameters = secondary_child_div.find('ul', {'class': 'offer-params__list'}) if secondary_child_div else None

    data = {
        'brand': '',
        'model': '',
        'year': '',
        'mileage': '',
        'engine_size': '',
        'fuel_type': '',
        'horse_power': '',
        'price': price,
        'ad_link': url,
        'src': photo_url
    }

    if parameters:
        items = parameters.find_all('li', {'class': 'offer-params__item'})
        labels = {
            'Marka pojazdu': 'brand',
            'Model pojazdu': 'model',
            'Rok produkcji': 'year',
            'Przebieg': 'mileage',
            'Pojemność skokowa': 'engine_size',
            'Rodzaj paliwa': 'fuel_type',
            'Moc': 'horse_power'
        }

        for item in items:
            label = item.find('span', {'class': 'offer-params__label'}).text.strip()
            value = item.find('div', {'class': 'offer-params__value'})

            if value:
                value = value.text.strip()

            if label in labels:
                data[labels[label]] = value

    return data


def scrape_otomoto(car_brand, MAX_LINKS):
    url_template = f'https://www.otomoto.pl/osobowe/{car_brand}?page={{}}'
    data = []

    for page_num in range(1, 999):
        url = url_template.format(page_num)
        links = get_ad_links(url)

        for link in links:
            ad_data = scrape_ad(link)

            if ad_data['brand'] and ad_data['model'] and ad_data['year'] and ad_data['mileage'] \
                    and ad_data['engine_size'] and ad_data['fuel_type'] and ad_data['horse_power']:
                data.append(ad_data)

            if len(data) >= MAX_LINKS:
                break

        if len(data) >= MAX_LINKS:
            break

    if len(data) < MAX_LINKS:
        print(f"Only {len(data)} offers found. Retrieving additional offers...")
        additional_links = get_ad_links(url_template.format(page_num + 1))

        for link in additional_links:
            ad_data = scrape_ad(link)

            if ad_data['brand'] and ad_data['model'] and ad_data['year'] and ad_data['mileage'] \
                    and ad_data['engine_size'] and ad_data['fuel_type'] and ad_data['horse_power']:
                data.append(ad_data)

            if len(data) >= MAX_LINKS:
                break

    return data[:MAX_LINKS]