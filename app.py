import os

from flask import Flask

from models import db
from routes import api

app = Flask(__name__)

POSTGRES = {
    'user': os.getenv('DB_USERNAME'),
    'pw': os.getenv('DB_PASSWORD'),
    'db': os.getenv('DB_NAME'),
    # For security reasons, secret/sensitive information should not be committed to a repository in a plain text file.
    # You should configure these details using environment variables, and then import them like the example above.
    # Environment variables can be created in the terminal as follows: $ export DB_USERNAME="database_username"
    'host': 'localhost',
    'port': '5432',
}

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db.init_app(app)
api.init_app(app)


@app.route("/")
def main():
    return 'Hello World !'

if __name__ == '__main__':
    app.run()
