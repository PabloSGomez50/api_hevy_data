from pydantic import BaseModel, ConfigDict
from typing import Optional, List
import datetime

class AddressBase(BaseModel):
    reference: Optional[str]
    zip_code: int
    province: str
    district: str

class AddressCreate(AddressBase):
    address: str

class Address(AddressBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int


class UserBase(BaseModel):
    firstname: str
    email: str
    verified: Optional[bool]

class UserCreate(UserBase):
    password: str

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    time_created: datetime.datetime
    time_updated: datetime.datetime = None
    addresses: List[Address] = []


class ProductPriceBase(BaseModel):
    product_id: int
    price: float

class ProductPriceCreate(ProductPriceBase):
    pass

class ProductPrice(ProductPriceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    time_created: datetime.datetime
    product: "Product"


class ProductBase(BaseModel):
    title: str
    url: str
    img_url: Optional[str] = None
    free_ship: Optional[bool] = False

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    prices: List[ProductPrice] = []