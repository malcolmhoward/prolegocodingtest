import os

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


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES


class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
