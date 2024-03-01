from sqlalchemy.sql import func
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, DateTime
from sqlalchemy.orm import relationship

from db.mysql import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
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
    title = Column(String(512))
    url = Column(String(512))
    img_url = Column(String(512), nullable=True)
    free_ship = Column(Boolean, default=False)

    prices = relationship("MLProductPrices", back_populates="product", cascade="all, delete-orphan")

class MLProductPrices(Base):
    __tablename__ = "ml_product_prices"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("ml_products.id"))
    price = Column(Float)
    time_created = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("MLProducts", back_populates="prices")