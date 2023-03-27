import requests
from bs4 import BeautifulSoup

import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="carprices",
    user="postgres",
    password="admin",
    port="5433"
)

cur = conn.cursor()
cur.execute("""
    TRUNCATE cars;
""")
conn.commit()

url_template = 'https://www.otomoto.pl/osobowe?page={}'

for page_num in range(1, 3):
    url = url_template.format(page_num)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    elements = soup.find_all('article', {'data-testid': 'listing-ad'})

    for element in elements:
        ad_title_h2 = element.find('h2', {'data-testid': 'ad-title'})
        ad_price_span = element.find('span', {'class': 'ooa-1bmnxg7 eayvfn611'})

        title_text = ad_title_h2.text.strip()
        price_text = ad_price_span.text.strip()

        ad_list_all = element.ul.find_all('li', {'class': 'ooa-1k7nwcr e19ivbs0'})

        try:
            year = ad_list_all[0].text.strip()
        except IndexError:
            year = ''
        try:
            mileage = ad_list_all[1].text.strip()
        except IndexError:
            mileage = ''
        try:
            engine_size = ad_list_all[2].text.strip()
        except IndexError:
            engine_size = ''
        try:
            fuel_type = ad_list_all[3].text.strip()
        except IndexError:
            fuel_type = ''

        cur.execute("""
            INSERT INTO cars (name, price, year, mileage, engine_size, fuel_type)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (title_text, price_text, year, mileage, engine_size, fuel_type))
        print(title_text, price_text, year, mileage, engine_size, fuel_type)
        conn.commit()

# TODO: Add a file ot send a query to a db (select)
