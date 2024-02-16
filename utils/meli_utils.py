import pandas as pd
import numpy as np
import requests
from lxml import html

ML_BASE_URL = "https://listado.mercadolibre.com.ar/"
ML_HEADERS = {
    'accept-language': 'es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5',
    'content-type': 'text/plain;charset=UTF-8',
    'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
}

def search_ml_posts(search_text: str) -> list:
    """
    Get the main info of the first page of MELI search page
    """

    r = requests.get(f"{ML_BASE_URL}/{search_text.replace(' ', '-')}", headers=ML_HEADERS)

    if r.ok:
        content = html.fromstring(r.text)
    else:
        print(f"ERROR MELI {r.status_code}: {r.text}")
        return []
    
    data = list()
    posts = content.xpath('//div[@class="ui-search-result__wrapper"]')

    for idx, post in enumerate(posts):
        retrieve = {}
        try:
            title_card = post.xpath('.//a[contains(@class,"ui-search-link__title-card")]')[0]
            retrieve['title'] = title_card.attrib.get("title")
            retrieve['link_to'] = title_card.attrib.get("href")
        except IndexError as e:
            print(f"Error getting post {idx}: {e}")
            continue
        try:
            retrieve['price'] = float(post.xpath('.//span[@class="andes-money-amount__fraction"]/text()')[0])
            shipping_card = post.xpath('.//div[contains(@class,"ui-search-item__group__element--shipping")]/p')
            retrieve['shipping'] = shipping_card[0].text if len(shipping_card) > 0 else "Standard shipping"

        except IndexError as e:
            print(f"Error getting ML info in {retrieve['title']}")
        except ValueError as e:
            print(f"No se pudo obtener el valor del item {retrieve['title']}")

        data.append(retrieve)

    return data