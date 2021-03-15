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
        print("Zipcode import started")

        db = Database()

        conn = pyodbc.connect(
            r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + os.getcwd() + '/watch/' + self.filename)
        cursor = conn.cursor()
        query = 'SELECT REPLACE(A13_POSTCODE, \' \', \'\'), A13_REEKSIND, CLng(A13_BREEKPUNT_VAN), ' \
                'CLng(A13_BREEKPUNT_TEM), A13_WOONPLAATS, A13_STRAATNAAM, CLng(A13_GEMEENTECODE) FROM POSTCODES'
        cursor.execute(query)

        # Create mass import
        # print("Importing zipcode data")
        # dbCursor = db.get_cursor()
        # query = "INSERT INTO zipcode (zipcode, series_index, breakpoint_from, breakpoint_to, town, street, muncipality_code) VALUES (?, ?, ?, ?, ?, ?, ?)"
        # dbCursor.executemany(query, data)
        # dbCursor.commit()

        # Create mass import
        query = "INSERT INTO zipcode (zipcode, series_index, breakpoint_from, breakpoint_to, town, street, muncipality_code) VALUES "

        print("Fetching zipcode data")

        i = 1
        for row in cursor.fetchall():
            if i == 1000:
                # # Remove last comma
                query = query[:-1]
                # Add head
                query += " INSERT INTO zipcode (zipcode, series_index, breakpoint_from, breakpoint_to, town, street, muncipality_code) VALUES "
                # Rest counter
                i = 1
            i += 1

            query += "("
            query += "'" + row[0] + "', "
            query += row[1] + ", "
            query += str(row[2]) + ", "
            query += str(row[3]) + ", "
            query += "'" + row[4].replace("'", "''") + "', "
            query += "'" + row[5].replace("'", "''") + "', "
            query += str(row[6])
            query += "),"

        # Execute query
        print("Importing zipcode data")
        response = db.execute(query + query[:-1])
        if not response:
            Logger().error("Something went wrong while importing zip codes")

