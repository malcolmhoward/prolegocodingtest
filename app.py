import os
from flask import Flask

from config import Config
from models import db
from routes import api

app = Flask(__name__)

app.config['DEBUG'] = True  # <-- TODO: This must be set to False in production/non-local environment.
# In debugging mode, a user of the application can execute arbitrary Python code on your computer.

app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
# app.config.from_object('config.Config')

db.init_app(app)
api.init_app(app)


@app.route("/")
def main():
    return 'Hello World!'

if __name__ == '__main__':
    # '0.0.0.0' tells Flask to listen for traffic from other devices on a network, in addition to localhost (127.0.0.1)
    app.run('0.0.0.0')
