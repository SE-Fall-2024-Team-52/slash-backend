from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database.database import Base


"""
Represents a user in the system.
Attributes:
    id (int): The primary key of the user.
    email (str): The unique email address of the user.
    username (str): The unique username of the user.
    first_name (str): The first name of the user.
    last_name (str): The last name of the user.
    hashed_password (str): The hashed password of the user.
    role (str): The role of the user - buyer or seller.
"""


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    role = Column(String)


"""
Represents a product being tracked for price changes.

Attributes:
    id (int): The primary key of the product.
    product_name (str): The name of the product.
    product_url (str): The URL of the product.
    site (str): The site where the product is listed.
    price (int): The current price of the product.
    currency (str): The currency of the product price.
    img_url (str): The URL of the product image.
"""


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


"""
Represents a product posting by a seller.

Attributes:
    id (int): The primary key of the product posting.
    name (str): The name of the product.
    posted_by (int): The ID of the user who posted the product.
    date_posted (str): The date when the product was posted.
    description (str): The description of the product.
    price (int): The price of the product.
    currency (str): The currency of the product price.
    sold (bool): Indicates whether the product has been sold.
"""


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


"""
Represents an item added to the wishlist by a user.

Attributes:
    id (int): The primary key of the wishlist item.
    user_id (int): The ID of the user who added the item to the wishlist.
    product_id (int): The ID of the product added to the wishlist.
    product_type (str): The type of the product added to the wishlist.
    date_added (str): The date when the product was added to the wishlist.
"""


class Wishlist(Base):
    __tablename__ = "wishlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    product_id = Column(Integer, ForeignKey("price_track_products.id"), index=True)
    product_type = Column(String)
    date_added = Column(String)


"""
Represents an item added to the shopping cart by a user.

Attributes:
    id (int): The primary key of the cart item.
    user_id (int): The ID of the user who added the item to the cart.
    product_id (int): The ID of the product added to the cart.
    product_type (str): The type of the product added to the cart.
    date_added (str): The date when the product was added to the cart.
"""


class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    product_id = Column(Integer, ForeignKey("price_track_products.id"), index=True)
    product_type = Column(String)
    date_added = Column(String)

"""
Represents an order placed by an user.

Attributes:
    id (int): The primary key of the order.
    user_id (int): The ID of the user who added the item to the cart.
    product_id (int): The ID of the product added to the cart.
    date_added (str): The date when the product was added to the cart.
"""
class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    product_id = Column(Integer, ForeignKey("price_track_products.id"), index=True)
    date_added = Column(String)
