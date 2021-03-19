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
            cursorAD = conn.cursor()
            cursorAD.execute('SELECT * FROM GEMEENTEN')

            # Create cursor queries
            header = "SET IDENTITY_INSERT muncipality ON " \
                     "INSERT INTO muncipality (muncipality_code, muncipality_name) VALUES "

            cursor = db.conn.cursor()
            exceptions = 0
            for row in cursorAD.fetchall():
                query = header + "("
                query += "'" + str(row[0]) + "', "
                query += "'" + row[1] + "'"
                query += "),"

                try:
                    cursor.execute(query)
                except Exception as e:
                    exceptions += 1

            cursor.commit()
            if exceptions > 0:
                Logger().error(str(exceptions) + " exceptions found while importing municipalities")
