from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)


class PriceTrackProducts(Base):
    __tablename__ = "price_track_products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    product_url = Column(String, index=True)
    site = Column(String)
    price = Column(Integer)
    currency = Column(String)
    img_url = Column(String)


class PriceTrackData(Base):
    __tablename__ = "price_track_data"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("price_track_products.id"))
    price = Column(Integer)
    currency = Column(String)
    date = Column(String)
    product_type = Column(String)


class ProductPostings(Base):
    __tablename__ = "product_postings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    posted_by = Column(Integer, ForeignKey("users.id"))
    date_posted = Column(String)
    description = Column(String)
    price = Column(Integer)
    currency = Column(String)
    sold = Column(Boolean)


class Wishlist(Base):
    __tablename__ = "wishlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    product_id = Column(Integer, ForeignKey("price_track_products.id"), index=True)
    product_type = Column(String)
    date_added = Column(String)
