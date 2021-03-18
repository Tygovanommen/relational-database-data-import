import os
import pyodbc
from src.database import Database
from src.logger import Logger


class Muncipality:
    # Filename + extension
    filename = None

    # Constructor to setup shop importer
    def __init__(self, filename):
        self.filename = filename

    # Process shop file
    def process(self):
        filepath = os.getcwd() + '/watch/' + self.filename
        if os.path.isfile(filepath):

            print("Muncipality import started")
    
            db = Database()

            conn = pyodbc.connect(
                r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + filepath)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM GEMEENTEN')

            # Create mass import
            query = "SET IDENTITY_INSERT muncipality ON INSERT INTO muncipality (muncipality_code, muncipality_name) VALUES "

            for row in cursor.fetchall():
                query += "("
                query += "'" + str(row[0]) + "', "
                query += "'" + row[1] + "'"
                query += "),"

            # Execute query
            response = db.execute(query[:-1])
            if not response:
                Logger().error("Something went wrong while importing municipalities")
