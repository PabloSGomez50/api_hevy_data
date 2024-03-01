from pydantic_models import ProductCreate, ProductPriceCreate


def test_product_create():

    product1 = ProductCreate(**{
        "title": "test",
        "url": "test",
        "img_url": "test",
        "free_ship": True,
    })
    assert product1.title == "test"
    assert product1.img_url == "test"
    assert product1.free_ship


    product2 = ProductCreate(**{
        "title": "test2",
        "url": "test3",
        "free_ship": False
    })
    assert product2.free_ship == False
    assert product2.url == "test3" 
    assert product2.img_url is None


    product3 = ProductCreate(**{
        "title": "test2",
        "url": "test",
        "free_ship": False,
        "price": 5.6
    })
    assert product3.img_url is None

    product4 = ProductCreate(**{
        "title": "test2",
        "url": "test",
        "price": 5.6
    })
    assert product4.img_url is None

def test_product_price_create():
    pprice = ProductPriceCreate(**{
        "product_id": 4,
        "title": "test2",
        "url": "test",
        "free_ship": False,
        "price": 5.6
    })
    assert round(pprice.price, 1) == round(5.6, 1)
