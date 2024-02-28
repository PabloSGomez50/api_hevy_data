from fastapi import Depends, APIRouter, HTTPException
from fastapi.security.api_key import APIKey
from sqlalchemy.orm import Session
import auth
import models.pydantic_models as schema
import models.sql_models as models
from db.mysql import get_db

meli_router = APIRouter()

@meli_router.get("/ml")
def get_products(api_key: APIKey = Depends(auth.get_api_key)):
    pass

@meli_router.get("/users/", response_model=list[schema.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    # api_key: APIKey = Depends(auth.get_api_key)
    ):
    users = db.query(models.User).offset(skip).limit(limit).all()

    if users is None:
        raise HTTPException(status_code=404, detail="Users not found")
    print(users)
    return users


@meli_router.post("/users/", response_model=schema.User)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db),
    # api_key: APIKey = Depends(auth.get_api_key)
    ):
    """
    Create user instance in database
    """
    if db.query(models.User).filter(models.User.email == user.email).first():
        return HTTPException(status_code=400, detail="User already exists")
    db_user = schema.User(**user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user