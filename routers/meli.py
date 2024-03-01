from fastapi import Depends, APIRouter, HTTPException
from fastapi.security.api_key import APIKey
from sqlalchemy.orm import Session
import auth
from views import meli as meli_views
import models.pydantic_models as schema
import models.sql_models as models
from db.mysql import get_db

meli_router = APIRouter(prefix="/ml")

@meli_router.get("/products")
def get_products(db: Session = Depends(get_db),
    # api_key: APIKey = Depends(auth.get_api_key)
    ):

    products =  db.query(models.MLProducts).all()

    return products

@meli_router.get("/users/", response_model=list[schema.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    # api_key: APIKey = Depends(auth.get_api_key)
    ):
    users = db.query(models.User).offset(skip).limit(limit).all()

    if users is None:
        raise HTTPException(status_code=404, detail="Users not found")
    print(users)
    for user in users:
        if user.time_updated is None:
            user.time_updated = user.time_created
    print(users[0].time_updated)
    return users


@meli_router.post("/users/", response_model=schema.User)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db),
    # api_key: APIKey = Depends(auth.get_api_key)
    ):
    """
    Create user instance in database
    """
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="User already exists")
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    if db_user.time_updated is None:
        db_user.time_updated = db_user.time_created
    return db_user


@meli_router.post("/product/add/{product_name}") #, response_model=list[schema.Product])
def create_product_by_name(product_name: str, db: Session = Depends(get_db),
    # api_key: APIKey = Depends(auth.get_api_key)
    ):
    """
    Create 
    """
    if db.query(models.MLProducts).filter(models.MLProducts.title.like(f"%{product_name}%")).first():
        raise HTTPException(status_code=400, detail="Products already exists")
    product_name_search = '-'.join(product_name.strip().split())
    print('Search for products', product_name_search)
    try:
        products_scrapped = meli_views.search_ml_posts(product_name_search)
    except Exception:
        raise HTTPException(status=500, detail="Can't get the products from Meli")

    # try:
    #     prices_scrapped = list()
    # except Exception:
    #     raise HTTPException()

    products_parsed = [schema.ProductCreate(**p_data)
        for p_data in products_scrapped
    ]
    db_products = [models.MLProducts(**p_data.model_dump())
        for p_data in products_parsed
    ]
    print('Loading to db')
    db.add_all(db_products)
    db.commit() 
    print('Loading product prices')
    db_prices = [models.MLProductPrices(product_id=p_id.id, price=p_data.get('price', 0.0))
        # **schema.ProductPriceCreate(**p_data).model_dump())
        for p_id, p_data in zip(db_products, products_scrapped)
    ]
    db.add_all(db_prices)
    db.commit()
    for product in db_products:
        db.refresh(product)
    # db.refresh(db_prices)
    # return db_products
    return {"detail": "Products inserted correctly"}


@meli_router.get("/product/{product_id}", response_model=schema.Product)
def fetch_ml_product_by_id(product_id: int, db: Session = Depends(get_db),
    # api_key: APIKey = Depends(auth.get_api_key)
    ):
    """
    Get Product from databes using product_id
    """

    product =  db.query(models.MLProducts).filter(models.MLProducts.id == product_id).first()
        
    return product

@meli_router.get("/product/search/{product_name}", response_model=list[schema.Product])
def fetch_ml_product_by_name(product_name: str, db: Session = Depends(get_db),
    # api_key: APIKey = Depends(auth.get_api_key)
    ):
    """
    Get Product from databes using product_name
    """

    products =  db.query(models.MLProducts).filter(
        models.MLProducts.title.like(f"%{product_name}%")
        ).all()
        
    return products