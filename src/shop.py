import os
import re

from src.database import Database
from src.logger import Logger


class Shop:

    # Constructor to setup shop importer
    def __init__(self, filename):
        self.db = Database()
        self.filename = filename
        self.filepath = os.getcwd() + "/watch/" + self.filename

    # Process shop file
    def process(self):
        if os.path.isfile(self.filepath):

            print("Shop import started")

            lines = self.__get_lines()
            if lines:
                self.__import_adress(lines)

    # Read data
    def __get_lines(self):
        lines = {}
        i = 0
        # Loop through lines
        with open(self.filepath, 'r') as r_file:
            for line in r_file:
                # Remove comments
                if line.startswith("--"):
                    continue

                # Go to next row
                if line == "\n":
                    i += 1
                    continue

                # Add line to array
                if not i in lines:
                    lines[i] = ""
                lines[i] += line.strip().replace(',', '') + ','

            return lines

    # Seperate housenumber from addition info
    def __get_adres_info(self, row):
        row = row.split(',')

        response = dict()

        # Clean data
        response['name'] = row[0]
        response['street'] = row[1]
        response['town'] = row[3]
        response['zipcode'] = row[5].replace(' ', '')
        response['phone_nr'] = row[6].replace(' ', '').replace('-', '')

        housenum = row[2].replace(' ', '').replace('/', '-')
        match = re.match(r"([0-9]+)([a-z]+)", housenum, re.I)
        if match:
            res = match.groups()
            response['house_nr'] = res[0]
            response['house_ad'] = res[1].upper()
        else:
            response['house_nr'] = housenum
            response['house_ad'] = ""

        return response

    # Import data to database
    def __import_adress(self, lines):

        # Create cursor queries
        header = "INSERT INTO adress (zipcode_id, house_nr, house_nr_addition) VALUES "

        cursor = self.db.get_connection().cursor()
        Logger().errors['Restaurants'] = dict()

        for key, value in lines.items():

            # Get adres info
            addressInfo = self.__get_adres_info(value[:-1])

            index = 0
            if (int(addressInfo['house_nr'].split('-')[0]) % 2) == 0:
                index = 1

            zipQuery = "SELECT id FROM zipcode WHERE series_index = " + str(index) + " AND zipcode = '" + addressInfo[
                'zipcode'] + "' AND " + addressInfo['house_nr'].split('-')[
                           0] + " BETWEEN breakpoint_from and breakpoint_to"

            query = header + "((" + zipQuery + "), '" + addressInfo['house_nr'] + "', '" + addressInfo[
                'house_ad'] + "')"

            try:
                cursor.execute(query)

                # Get last ID
                cursor.execute("SELECT @@IDENTITY AS ID;")
                address_id = cursor.fetchone()[0]

                # Import restaurant
                query = "INSERT INTO restaurant (adress_id, name, phone_nr) VALUES"
                query += "(" + str(address_id) + ", '" + addressInfo['name'] + "', " + addressInfo['phone_nr'] + ")"

                cursor.execute(query)

            except Exception as e:
                code = e.args[0]
                if code in Logger().errors['Restaurants']:
                    Logger().errors['Restaurants'][code] += 1
                else:
                    Logger().errors['Restaurants'][code] = 1

        cursor.commit()
