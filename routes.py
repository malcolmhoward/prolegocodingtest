from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser

api = Api(prefix="/api/v1")

# TODO: Use this hard-coded application data for unit tests
applications = [
    {
        'application_id': '11193',
        'first_name': 'Jack',
        'last_name': 'Chorce',
        'date_of_birth': '1/15/1967',
        'application_start_date': '3/12/2018',
        'underwriting_start_date': '4/12/2018',
        'document_request_start_date': '4/15/2018',
        'all_documents_received_date': '4/29/2018',
        'underwriting_complete_date': '5/1/2018',
        'underwriting_cycle_time': 19,
        'application_approved': False
    },
    {
        'application_id': '13900',
        'first_name': 'Ann',
        'last_name': 'Marvens',
        'date_of_birth': '3/4/1970',
        'application_start_date': '3/25/2018',
        'underwriting_start_date': '3/27/2018',
        'document_request_start_date': '4/27/2018',
        'all_documents_received_date': '5/7/2018',
        'underwriting_complete_date': '5/29/2018',
        'underwriting_cycle_time': 63,
        'application_approved': True
    },
]

def get_application_by_id(application_id, use_database=False):
    application_id = int(application_id)
    application_data = {}

    # Use the hard-coded test data
    # TODO: Consider performance tuning
    for data in applications:
        if int(data.get("application_id", 0)) == application_id:
            application_data = data
            break

    return application_data

# Configure a parser to validate incoming data
application_request_parser = RequestParser(bundle_errors=True)
application_request_parser.add_argument("application_id", type=str, required=True, help="Please enter valid integer as ID")
application_request_parser.add_argument("first_name", type=str, required=True, help="First name has to be valid string")
application_request_parser.add_argument("last_name", type=str, required=True, help="Last name has to be valid string")
application_request_parser.add_argument("date_of_birth", type=str, required=True, help="Date needs to be in format of dd/mm/yyyy")
application_request_parser.add_argument("application_start_date", type=str, required=True, help="Date needs to be in format of dd/mm/yyyy")
application_request_parser.add_argument("underwriting_start_date", type=str, required=True, help="Date needs to be in format of dd/mm/yyyy")
application_request_parser.add_argument("document_request_start_date", type=str, required=True, help="Date needs to be in format of dd/mm/yyyy")
application_request_parser.add_argument("all_documents_received_date", type=str, required=False, help="Date needs to be in format of dd/mm/yyyy")
application_request_parser.add_argument("underwriting_complete_date", type=str, required=False, help="Date needs to be in format of dd/mm/yyyy")
application_request_parser.add_argument("underwriting_cycle_time", type=int, required=False, help="Please enter valid integer as ID")
application_request_parser.add_argument("application_approved", type=bool, required=True, help="Please enter True or False")


class ApplicationCollection(Resource):
    def get(self):
        application_data = {
            'msg': "List data for all application instances",
            'count': len(applications),
            'results': applications
        }

        return application_data

    def post(self):
        args = application_request_parser.parse_args()
        applications.append(args)

        return {"msg": "The application instance was created", "application_data": args}, 201


class Application(Resource):
    def get(self, id):
        # return {"msg": "Details about application instance where application_id={}".format(id)}
        application = get_application_by_id(id)
        if not application:
            return {"error": "Application not found"}

        return application

    def put(self, id):
        # return {"msg": "Update application instance where application_id={}".format(id)}
        args = application_request_parser.parse_args()
        application = get_application_by_id(id)
        if application:
            applications.remove(application)
            applications.append(args)

        return args

    def delete(self, id):
        # return {"msg": "Delete application instance where application_id={}".format(id)}
        application = get_application_by_id(id)
        if application:
            applications.remove(application)

        return {"message": "Deleted"}, 204


api.add_resource(ApplicationCollection, '/applications')
api.add_resource(Application, '/applications/<int:id>')

# TODO: Implement collection and detail resources for a second model
