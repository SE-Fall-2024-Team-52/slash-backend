from flask import Flask
from database.database import engine

import database.models as models

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    app.run(debug=True)
