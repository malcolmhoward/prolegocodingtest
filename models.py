from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.state import InstanceState
import datetime

db = SQLAlchemy()


class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self.__dict__.items()
        })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects.
                InstanceState is not JSON serializable, so exclude it
        """
        formatted_data = {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self.__dict__.items() if not isinstance(value, InstanceState)
        }

        return formatted_data


class Application(BaseModel, db.Model):
    """Model for the application table"""
    # __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, nullable=False)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    application_start_date = db.Column(db.Date, nullable=False)
    underwriting_start_date = db.Column(db.Date, nullable=False)
    document_request_start_date = db.Column(db.Date, nullable=False)
    all_documents_received_date = db.Column(db.Date)
    underwriting_complete_date = db.Column(db.Date)
    underwriting_cycle_time = db.Column(db.Integer)
    application_approved = db.Column(db.Boolean, nullable=False)
    # TODO: **Required** Derive all_documents_received_cycle_time field from the existing columns in this model
    # TODO: **Optional** Derive additional fields

# TODO: **Optional** Implement a second model based on the data in the second CSV
