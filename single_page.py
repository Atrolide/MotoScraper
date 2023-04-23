import requests
from bs4 import BeautifulSoup


def scrapeOlx(link):
    brand, model, year, mileage, engine_size, fuel_type, horse_power = [], [], [], [], [], [], []
    url = link
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    brand = soup.find_all('a', class_='css-tyi2d1')[3].text.strip()
    elements = soup.find_all('p', class_='css-b5m1rv er34gjf0')
    for element in elements:
        if 'Model: ' in element.text:
            model = element.text.strip()
            word_to_remove = "Model: "
            model = model.replace(word_to_remove, "")

        if 'Rok produkcji: ' in element.text:
            year = element.text.strip()
            word_to_remove = "Rok produkcji: "
            year = year.replace(word_to_remove, "")

        if 'Przebieg: ' in element.text:
            mileage = element.text.strip()
            word_to_remove = "Przebieg: "
            mileage = mileage.replace(word_to_remove, "")

        if 'Poj. silnika: ' in element.text:
            engine_size = element.text.strip()
            word_to_remove = "Poj. silnika: "
            engine_size = engine_size.replace(word_to_remove, "")

        if 'Paliwo: ' in element.text:
            fuel_type = element.text.strip()
            word_to_remove = "Paliwo: "
            fuel_type = fuel_type.replace(word_to_remove, "")

        if 'Moc silnika: ' in element.text:
            horse_power = element.text.strip()
            word_to_remove = "Moc silnika: "
            horse_power = horse_power.replace(word_to_remove, "")

    return [brand, model, year, mileage, engine_size, fuel_type, horse_power]
