from collections import OrderedDict

from flask_script import Manager
from flask_script.commands import Command
from flask_migrate import Migrate, MigrateCommand

from app import app, db
from models import Application
from routes import APPLICATIONS, application_table, engine


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


class LoadDatabase(Command):
    """
    Reads data from the CSV, and loads each row as a new record in the Application model.
    """
    def run(self):
        self.load_database()

    def load_database(self):
        f = open("Coding test for CSV file - Sheet1.csv", "r")
        # Read the content from the file, and split on newline character to create a list of row data strings
        contents_list = f.read().split('\n')
        column_names = APPLICATIONS[0].keys()
        num_rows_added = 0
        for index, row_data_string in enumerate(contents_list):
            # Assumption: The first road is the heading, and has no data we need, so it can be skipped.
            if index != 0:
                row_data = row_data_string.split(',')
                # Use a list comprehension to remove the leading and trailing whitespace around the data
                trimmed_row_data = [data.strip() for data in row_data]
                # Replace the Not a Number acronym with None so that it can be saved in the database as a null value
                cleaned_row_data = [None if data == 'NaN' else data for data in trimmed_row_data]
                data = OrderedDict(zip(column_names, cleaned_row_data))
                # Transform the application_approved field value from numerical to boolean
                data['application_approved'] = False if data['application_approved'] in [0, '0'] else True
                con = engine.connect()
                # TODO: **Optional** Add some exception handling to this database insert command, just in case it fails
                con.execute(application_table.insert(), **data)
                num_rows_added += 1
        print('{} records added to the Application table'.format(num_rows_added))
        print("load_database management command completed")


class ClearDatabase(Command):
    """
    Removes all Application records from the CSV
    """
    def run(self):
        self.clear_database()

    def clear_database(self):
        num_rows_deleted = 0
        try:
            num_rows_deleted = db.session.query(Application).delete()
            db.session.commit()
        except:
            db.session.rollback()
            # TODO: **Optional** Capture some meaningful information about the error, and add it to the error message
            print('Unknown error occurred.')
        print('{} records were deleted from the Application table'.format(num_rows_deleted))
        print("clear_database management command completed")


# TODO: **Optional** Expose the load_database() and clear_database() methods via the API
manager.add_command("load_database", LoadDatabase())
manager.add_command("clear_database", ClearDatabase())

if __name__ == "__main__":
    manager.run()

