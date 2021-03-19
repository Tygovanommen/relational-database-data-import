import os
import re

from src.database import Database
from src.logger import Logger


class Shop:
    # Filename + extension
    filename = None

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
                self.__import_restaurant(lines)

    # Read data
    def __get_lines(self):
        lines = {}
        i = 0
        with open(self.filepath, 'r') as r_file:
            # Loop through lines
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

    # Import data to database
    def __import_adress(self, lines):

        # Create cursor queries
        header = "INSERT INTO adress (zipcode, house_nr, house_nr_addition) VALUES "

        cursor = self.db.get_connection().cursor()
        exceptions = 0
        for key, value in lines.items():

            # Get adres info
            row = value[:-1].split(',')
            adresInfo = self.__get_adres_info(row)

            query = header + "('" + adresInfo['zipcode'] + "', '" + adresInfo['house_nr'] + "', '" + adresInfo[
                'house_ad'] + "')"

            try:
                cursor.execute(query)
            except Exception as e:
                exceptions += 1

        cursor.commit()
        if exceptions > 0:
            Logger().error(str(exceptions) + " exceptions found while importing addresses")


    def __import_restaurant(self, lines):

        # Create cursor queries
        header = "INSERT INTO restaurant (adress_id, name, phone_nr) VALUES "

        cursor = self.db.get_connection().cursor()
        exceptions = 0
        for key, value in lines.items():

            # Get adres info
            row = value[:-1].split(',')
            adresInfo = self.__get_adres_info(row)

            query = header + "((SELECT id FROM adress WHERE zipcode = '" + adresInfo['zipcode'] + "' AND house_nr = '" + \
                     adresInfo['house_nr'] + "' AND house_nr_addition = '" + adresInfo[
                         'house_ad'] + "'), '" + row[0] + "', " + adresInfo['phone_nr'] + ")"

            try:
                cursor.execute(query)
            except Exception as e:
                exceptions += 1

        cursor.commit()
        if exceptions > 0:
            Logger().error(str(exceptions) + " exceptions found while importing restaurants")


    # Seperate housenumber from addition info
    def __get_adres_info(self, row):
        response = dict()

        response['zipcode'] = row[5].replace(' ', '')
        response['phone_nr'] = row[6].replace(' ', '').replace('-', '')

        housenum = row[2].replace(' ', '')
        match = re.match(r"([0-9]+)([a-z]+)", housenum, re.I)
        if match:
            res = match.groups()
            response['house_nr'] = res[0]
            response['house_ad'] = res[1]
        else:
            response['house_nr'] = housenum
            response['house_ad'] = ""

        return response
