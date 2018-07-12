import os
from flask import Flask

from config import Config
from models import db
from routes import api

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
# app.config.from_object('config.Config')

db.init_app(app)
api.init_app(app)


@app.route("/")
def main():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
