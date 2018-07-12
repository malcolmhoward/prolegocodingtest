from flask_restful import Resource, Api

api = Api(prefix="/api/v1")

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


class ApplicationCollection(Resource):
    def get(self):
        return {"msg": "List data for all application instances"}

    def post(self):
        return {"msg": "Create new application instance here"}


class Application(Resource):
    def get(self, id):
        return {"msg": "Details about application instance where application_id={}".format(id)}

    def put(self, id):
        return {"msg": "Update application instance where application_id={}".format(id)}

    def delete(self, id):
        return {"msg": "Delete application instance where application_id={}".format(id)}


api.add_resource(ApplicationCollection, '/applications')
api.add_resource(Application, '/applications/<int:id>')

# TODO: Implement collection and detail resources for a second model
