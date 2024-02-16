import pandas as pd
import numpy as np
import requests
from lxml import html

ML_BASE_URL = "https://listado.mercadolibre.com.ar/"
ML_HEADERS = {

}

def search_ml_posts(search_text: str) -> list:
    """
    Get the main info of the first page of MELI search page
    """

    r = requests.get(f"{ML_BASE_URL}/{search_text.replace(' ', '-')}", headers=ML_HEADERS)
    # print(r.text)
    if r.ok:
        content = html.fromstring(r.text)
    else:
        print(f"ERROR MELI {r.status_code}: {r.text}")
        return []
    
    data = list()
    posts = content.xpath('//div[@class="ui-search-result__wrapper"]')
    print("Posts", len(posts))
    for idx, post in enumerate(posts[:5]):
        retrieve = {}
        try:
            title_card = post.xpath('//div[@class="ui-search-item__group--title"]/a')[0]
            retrieve['title'] = title_card.text
            retrieve['link_to'] = title_card.href
        except IndexError as e:
            print(f"Error getting post {idx}: {e}")
            continue
        try:
            retrieve['price'] = post.xpath('//span[@class="andres-money-amount__fraction"]')[0].text
            shipping_card = post.xpath('//div[@class="ui-search-item__group--shipping"]')
            retrieve['shipping'] = shipping_card[0].text if len(shipping_card) > 0 else "Standard shipping"

        except IndexError as e:
            print(f"Error getting ML info in {retrieve['title']}")

        data.append(retrieve)

    return data