import requests
from bs4 import BeautifulSoup
import re

def scrapeOlx(link):
    brand, model, year, mileage, engine_size, fuel_type, horse_power, price = [], [], [], [], [], [], [], []
    url = link
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    brand = soup.find_all('a', class_='css-tyi2d1')[3].text.strip()
    price = soup.find_all('h3', class_='css-ddweki er34gjf0')[0].text.strip()
    price = price.replace("zł", "PLN")
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
            fuel_type = re.sub(r'\bbenzyna\b', 'Gasoline', fuel_type, flags=re.IGNORECASE)
            fuel_type = re.sub(r'\bhybryda\b', 'hybrid', fuel_type, flags=re.IGNORECASE)

        if 'Moc silnika: ' in element.text:
            horse_power = element.text.strip()
            word_to_remove = "Moc silnika: "
            horse_power = horse_power.replace(word_to_remove, "")


        # Find all image tags
    img_tags = soup.find_all('img')

    # Extract src attribute from each image tag
    src_list = []
    for img in img_tags:
        src = img.get('src')
        if src:
            src_list.append(src)
            break

    return [brand, model, year, mileage, engine_size, fuel_type, horse_power, price, src_list]


