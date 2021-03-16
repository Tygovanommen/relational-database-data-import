import os
import pyodbc
from src.database import Database
from src.logger import Logger


class ZipCode:
    # Filename + extension
    filename = None

    # Constructor to setup shop importer
    def __init__(self, filename):
        self.filename = filename

    # Process shop file
    def process(self):
        print("Zipcode process started")

        db = Database()

        conn = pyodbc.connect(
            r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + os.getcwd() + '/watch/' + self.filename)
        cursor = conn.cursor()
        query = 'SELECT REPLACE(A13_POSTCODE, \' \', \'\'), ABS(CBool(A13_REEKSIND)), CLng(A13_BREEKPUNT_VAN), ' \
                'CLng(A13_BREEKPUNT_TEM), A13_WOONPLAATS, A13_STRAATNAAM, CLng(A13_GEMEENTECODE) FROM POSTCODES'
        cursor.execute(query)
        data = cursor.fetchall()

        # Create mass import
        print("Importing zipcode data")
        dbCursor = db.get_cursor()
        dbCursor.fast_executemany = True

        # Create mass import
        query = "INSERT INTO zipcode (zipcode, series_index, breakpoint_from, breakpoint_to, town, street, muncipality_code) VALUES (?, ?, ?, ?, ?, ?, ?)"
        dbCursor.executemany(query, data)
        dbCursor.commit()
