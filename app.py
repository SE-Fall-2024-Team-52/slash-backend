from fastapi import Depends
from flask import Flask, request, jsonify
from database.database import engine, db_session
from util.hashing import get_hashed_password, verify_password
from sqlalchemy.orm import Session
import database.models as models
from flask_cors import CORS
from datetime import datetime


app = Flask(__name__)
CORS(app)
# app.config.from_pyfile("settings.py")


@app.route("/", methods=["GET", "POST"])
def hello():
    return get_hashed_password("password", "username")


@app.route("/postings/<username>", methods=["GET"])
def get_postings(username):
    validation1 = (
        db_session.query(models.Users).filter(models.Users.username == username).first()
    )
    if validation1 is None:
        return jsonify(
            content={"status": "error", "message": f"User {username} does not exist"}
        )
    products = (
        db_session.query(models.ProductPostings)
        .filter(models.ProductPostings.posted_by == validation1.id)
        .all()
    )
    return jsonify(
        content={
            "status": "success",
            "data": [
                {
                    "name": product.name,
                    "date_posted": product.date_posted,
                    "description": product.description,
                    "price": product.price,
                    "currency": product.currency,
                    "sold": product.sold,
                    "posted_by": f"{validation1.first_name} {validation1.last_name}",
                }
                for product in products
            ],
        }
    )


@app.route("/add-posting", methods=["POST"])
def add_posting():

    name = request.json.get("name")
    description = request.json.get("description")
    price = request.json.get("price")
    currency = request.json.get("currency")
    username = request.json.get("username")
    today_date = datetime.today().strftime("%Y-%m-%d")

    validation1 = (
        db_session.query(models.Users).filter(models.Users.username == username).first()
    )
    if validation1 is None:
        return jsonify(
            content={"status": "error", "message": f"User {username} does not exist"}
        )

    new_product = models.ProductPostings(
        name=name,
        description=description,
        price=price,
        currency=currency,
        date_posted=today_date,
        posted_by=validation1.id,
        sold=False,
    )
    db_session.add(new_product)
    db_session.commit()

    return jsonify(
        content={
            "status": "success",
        }
    )


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = (
        db_session.query(models.Users).filter(models.Users.username == username).first()
    )

    if user is None:
        return jsonify(content={"status": "error", "message": "User does not exist"})

    if not verify_password(password, user.hashed_password):
        return jsonify(
            content={
                "status": "error",
                "message": "Invalid password",
            }
        )

    return jsonify(
        content={
            "status": "success",
            "message": "User successfully logged in",
            "data": {
                "username": user.username,
                "email": user.email,
                "firstname": user.first_name,
                "lastname": user.last_name,
            },
        }
    )


@app.route("/register", methods=["POST"])
def register_user():
    username = request.json.get("username")
    email = request.json.get("email")
    firstname = request.json.get("firstname")
    lastname = request.json.get("lastname")
    password = request.json.get("password")

    validation1 = (
        db_session.query(models.Users).filter(models.Users.username == username).first()
    )

    validation2 = (
        db_session.query(models.Users).filter(models.Users.email == email).first()
    )

    if validation1 is not None:
        return jsonify(content={"status": "error", "message": "Username already taken"})
    if validation2 is not None:
        return jsonify(content={"status": "error", "message": "Email-id already taken"})

    user_model = models.Users()
    user_model.username = username
    user_model.email = email
    user_model.first_name = firstname
    user_model.last_name = lastname
    hash_password = get_hashed_password(password)
    user_model.hashed_password = hash_password
    db_session.add(user_model)
    db_session.commit()

    return jsonify(
        content={
            "status": "success",
            "message": "User successfully created",
            "data": {
                "username": username,
                "email": email,
                "firstname": firstname,
                "lastname": lastname,
            },
        }
    )


models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    app.run(debug=True)
