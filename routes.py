from collections import OrderedDict
# from flask.json import jsonify

from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser

from sqlalchemy import create_engine, MetaData, Table

from config import Config
from models import Application as ApplicationModel

api = Api(prefix="/api/v1")

# TODO: **Optional** Use this hard-coded application data for unit tests
APPLICATIONS = [
    OrderedDict([
        ('application_id', 11193),
        ('first_name', 'Jack'),
        ('last_name', 'Chorce'),
        ('date_of_birth', '1/15/1967'),
        ('application_start_date', '3/12/2018'),
        ('underwriting_start_date', '4/12/2018'),
        ('document_request_start_date', '4/15/2018'),
        ('all_documents_received_date', '4/29/2018'),
        ('underwriting_complete_date', '5/1/2018'),
        ('underwriting_cycle_time', 19),
        ('application_approved', False)
    ]),
    OrderedDict({
        ('application_id', 13900),
        ('first_name', 'Ann'),
        ('last_name', 'Marvens'),
        ('date_of_birth', '3/4/1970'),
        ('application_start_date', '3/25/2018'),
        ('underwriting_start_date', '3/27/2018'),
        ('document_request_start_date', '4/27/2018'),
        ('all_documents_received_date', '5/7/2018'),
        ('underwriting_complete_date', '5/29/2018'),
        ('underwriting_cycle_time', 63),
        ('application_approved', True)
    })
]

# The above notation results in the following dictionaries, with key order guaranteed, unlike normal dictionaries
# APPLICATIONS = [
#     {
#         'application_id': 11193,
#         'first_name': 'Jack',
#         'last_name': 'Chorce',
#         'date_of_birth': '1/15/1967',
#         'application_start_date': '3/12/2018',
#         'underwriting_start_date': '4/12/2018',
#         'document_request_start_date': '4/15/2018',
#         'all_documents_received_date': '4/29/2018',
#         'underwriting_complete_date': '5/1/2018',
#         'underwriting_cycle_time': 19,
#         'application_approved': False
#     },
#     {
#         'application_id': 13900,
#         'first_name': 'Ann',
#         'last_name': 'Marvens',
#         'date_of_birth': '3/4/1970',
#         'application_start_date': '3/25/2018',
#         'underwriting_start_date': '3/27/2018',
#         'document_request_start_date': '4/27/2018',
#         'all_documents_received_date': '5/7/2018',
#         'underwriting_complete_date': '5/29/2018',
#         'underwriting_cycle_time': 63,
#         'application_approved': True
#     },
# ]

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, convert_unicode=True)
metadata = MetaData(bind=engine)
application_table = Table('application', metadata, autoload=True)


def get_application_by_id(application_id, use_database=False):
    # application_id shouldn't be a string at this point, but maybe it doesn't hurt to cast it to an int just in case
    application_id = int(application_id)
    application_data = {}
    if use_database:
        # Query the application table to find the data to be returned
        application_data = ApplicationModel.query.filter(ApplicationModel.application_id == application_id).first().json()
    else:
        # Use the hard-coded test data
        # TODO: **Optional** Consider performance tuning
        for data in APPLICATIONS:
            if int(data.get("application_id", 0)) == application_id:
                application_data = data
                break

    return application_data


def get_use_database(querystring_args):
    use_database = False if querystring_args.get('use_database', None) in [None, False, 'False', 'false'] else True

    return use_database

# Configure a parser to validate incoming Application POST data
application_request_parser = RequestParser(bundle_errors=True)
application_request_parser.add_argument('application_id', type=int, required=True, help="Please enter valid integer as ID")
application_request_parser.add_argument('first_name', type=str, required=True, help="First name has to be valid string")
application_request_parser.add_argument('last_name', type=str, required=True, help="Last name has to be valid string")
application_request_parser.add_argument('date_of_birth', type=str, required=True, help="Date needs to be in format of dd/mm/yyyy")
application_request_parser.add_argument('application_start_date', type=str, required=True, help="Date needs to be in format of dd/mm/yyyy")
application_request_parser.add_argument('underwriting_start_date', type=str, required=True, help="Date needs to be in format of dd/mm/yyyy")
application_request_parser.add_argument('document_request_start_date', type=str, required=True, help="Date needs to be in format of dd/mm/yyyy")
application_request_parser.add_argument('all_documents_received_date', type=str, required=False, help="Date needs to be in format of dd/mm/yyyy")
application_request_parser.add_argument('underwriting_complete_date', type=str, required=False, help="Date needs to be in format of dd/mm/yyyy")
application_request_parser.add_argument('underwriting_cycle_time', type=int, required=False, help="Please enter valid integer as ID")
application_request_parser.add_argument('application_approved', type=bool, required=True, help="Please enter True or False")

# Configure a parser to handle incoming data in the querystring
application_request_querystring_parser = RequestParser(bundle_errors=True)
application_request_querystring_parser.add_argument('use_database', required=False)


class ApplicationCollection(Resource):
    def get(self):
        querystring_args = application_request_querystring_parser.parse_args()
        use_database = get_use_database(querystring_args=querystring_args)
        applications = APPLICATIONS
        if use_database:
            applications = [application.json() for application in ApplicationModel.query.all()]
        application_data = {
            'msg': "List data for all application instances",
            'count': len(applications),
            'results': applications
        }

        return application_data

    def post(self):
        args = application_request_parser.parse_args()
        querystring_args = application_request_querystring_parser.parse_args()
        use_database = get_use_database(querystring_args=querystring_args)
        if use_database:
            con = engine.connect()
            con.execute(application_table.insert(), **args)
        else:
            APPLICATIONS.append(args)

        return {"msg": "The application instance was created", "application_data": args}, 201


class Application(Resource):
    def get(self, obj_id):
        # return {"msg": "Details about application instance where application_id={}".format(id)}
        querystring_args = application_request_querystring_parser.parse_args()
        use_database = get_use_database(querystring_args=querystring_args)
        application = get_application_by_id(obj_id, use_database)
        if not application:
            return {"error": "Application not found"}

        return application

    def put(self, obj_id):
        """
        This accepts the normal POST payload.  The standard POST args are required, & partial updates are not supported.
        :param obj_id:
        :return:
        """
        # return {"msg": "Update application instance where application_id={}".format(id)}
        args = application_request_parser.parse_args()
        querystring_args = application_request_querystring_parser.parse_args()
        use_database = get_use_database(querystring_args=querystring_args)
        application = get_application_by_id(obj_id, use_database)
        if application:
            if use_database:
                con = engine.connect()
                # TODO: Figure out why this update command updates all of the records in the table instead of an individual row
                con.execute(application_table.update(), **args)
            else:
                # TODO: **Optional** Add support for updating a partial argument list for a given application
                APPLICATIONS.remove(application)
                APPLICATIONS.append(args)

        return args

    def delete(self, obj_id):
        # return {"msg": "Delete application instance where application_id={}".format(id)}
        args = application_request_parser.parse_args()
        querystring_args = application_request_querystring_parser.parse_args()
        use_database = get_use_database(querystring_args=querystring_args)
        application = get_application_by_id(obj_id, use_database)
        if application:
            if use_database:
                con = engine.connect()
                con.execute(application_table.delete(), **args)
            else:
                # TODO: **Optional** Add support for removing a given application simply by URL (i.e. no request payload)
                APPLICATIONS.remove(application)

        return {"message": "Deleted"}, 204


api.add_resource(ApplicationCollection, '/applications')
api.add_resource(Application, '/applications/<int:obj_id>')

# TODO: **Optional** Implement collection and detail resources/routes for a second model
