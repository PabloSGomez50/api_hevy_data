from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from db.mysql import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    firstname = Column(String(64))
    email = Column(String(64), unique=True, index=True)
    password = Column(String(256))
    verified = Column(Boolean, default=False)

    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f'User {self.id}: {self.email}|{self.firstname}'

class Address(Base):
    __tablename__ = "user_address"

    id = Column(Integer, primary_key=True)
    address = Column(String(128))
    reference = Column(String(256), nullable=True)
    zip_code = Column(Integer)
    province = Column(String(64))
    district = Column(String(64))
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="addresses")

class MLProducts(Base):
    __tablename__ = 'ml_products'

    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    url = Column(String(256))
    img_url = Column(String(256))
    free_ship = Column(Boolean, default=False)