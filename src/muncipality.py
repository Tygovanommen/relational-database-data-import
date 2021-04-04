import os
from collections import defaultdict

import pyodbc
from src.database import Database
from src.logger import Logger


class Muncipality:

    # Constructor to setup shop importer
    def __init__(self, filename):
        self.filename = filename
        self.db = Database()

    # Process shop file
    def process(self):
        filepath = os.getcwd() + '/watch/' + self.filename
        if os.path.isfile(filepath):

            print("Muncipality import started")

            conn = pyodbc.connect(
                r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + filepath)
            cursorAD = conn.cursor()
            cursorAD.execute('SELECT * FROM GEMEENTEN')

            # Create cursor queries
            header = "SET IDENTITY_INSERT muncipality ON " \
                     "INSERT INTO muncipality (muncipality_code, muncipality_name) VALUES "

            cursor = self.db.conn.cursor()
            Logger().errors['Muncipalities'] = dict()
            for row in cursorAD.fetchall():
                query = header + "("
                query += "'" + str(row[0]) + "', "
                query += "'" + row[1] + "'"
                query += ")"

                try:
                    cursor.execute(query)
                except Exception as e:
                    code = e.args[0]
                    if code in Logger().errors['Muncipalities']:
                        Logger().errors['Muncipalities'][code] += 1
                    else:
                        Logger().errors['Muncipalities'][code] = 1

            cursor.commit()

