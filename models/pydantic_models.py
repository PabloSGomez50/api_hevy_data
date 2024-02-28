from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class UserBase(BaseModel):
    firstname: str
    email: str

class AddressBase(BaseModel):
    reference: Optional[str]
    zip_code: int
    province: str
    district: str

class UserCreate(UserBase):
    password: str

class AddressCreate(AddressBase):
    address: str

class Address(AddressBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    verified: Optional[bool]
    addresses: List[Address] = []