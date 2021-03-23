import os
import pyodbc
from src.database import Database
from src.logger import Logger


class ZipCode:

    # Constructor to setup shop importer
    def __init__(self, filename):
        self.filename = filename
        self.db = Database()

    # Process shop file
    def process(self):
        filepath = os.getcwd() + '/watch/' + self.filename
        if os.path.isfile(filepath):

            print("Zipcode process started")

            conn = pyodbc.connect(
                r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + filepath)
            cursor = conn.cursor()
            query = 'SELECT REPLACE(A13_POSTCODE, \' \', \'\'), ABS(CBool(A13_REEKSIND)), CLng(A13_BREEKPUNT_VAN), ' \
                    'CLng(A13_BREEKPUNT_TEM), A13_WOONPLAATS, A13_STRAATNAAM, CLng(A13_GEMEENTECODE) FROM POSTCODES'
            cursor.execute(query)
            data = cursor.fetchall()

            # Create mass import
            print("Importing zipcode data")
            dbCursor = self.db.get_cursor()
            dbCursor.fast_executemany = True

            # Create ghost table
            ghostTableQuery = "IF OBJECT_ID('zipcode_ghost') IS NOT NULL DROP TABLE zipcode_ghost; " \
                              "CREATE TABLE zipcode_ghost (" \
                              "zipcode          varchar(6)   not null," \
                              "series_index     bit          not null," \
                              "breakpoint_from  int          not null," \
                              "breakpoint_to    int          not null," \
                              "town             varchar(255) not null," \
                              "street           varchar(255) not null," \
                              "muncipality_code smallint     not null)"
            dbCursor.execute(ghostTableQuery)

            # Create mass import
            query = "INSERT INTO zipcode_ghost (zipcode, series_index, breakpoint_from, breakpoint_to, town, street, muncipality_code) VALUES (?, ?, ?, ?, ?, ?, ?)"
            try:
                dbCursor.executemany(query, data)
                dbCursor.commit()
            except Exception as e:
                Logger().errors['Zipcodes'] = "Error while importing zipcodes: " + str(e)

            dbCursor.execute("exec zipcode_import")
