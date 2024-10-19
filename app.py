from fastapi import Depends
from flask import Flask, request, jsonify
from database.database import engine, db_session
from util.hashing import get_hashed_password, verify_password
from sqlalchemy.orm import Session
import database.models as models

app = Flask(__name__)

# app.config.from_pyfile("settings.py")


@app.route("/", methods=["GET", "POST"])
def hello(request):
    return get_hashed_password("password", "username")


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
        db_session.query(models.Users).filter(models.Users.username == "some").first()
    )

    validation2 = (
        db_session.query(models.Users).filter(models.Users.email == "some").first()
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
