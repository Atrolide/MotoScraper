import requests
from bs4 import BeautifulSoup


def get_ad_links(car_brand, MAX_LINKS):
    links = []
    if car_brand:
        url_template = f'https://www.olx.pl/motoryzacja/samochody/{car_brand}/?page={{}}'
    else:
            url_template = f'https://www.olx.pl/motoryzacja/samochody?page={{}}'
    page_num = 1
    retrieved_links = 0

    while retrieved_links < MAX_LINKS:
        url = url_template.format(page_num)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        for div in soup.find_all("div", {"data-cy": "l-card"}):
            link = div.find("a")["href"]
            if '/d/' in link:
                links.append('https://www.olx.pl' + link)
                retrieved_links += 1

                if retrieved_links >= MAX_LINKS:
                    break

        page_num += 1

    return links[:MAX_LINKS]
