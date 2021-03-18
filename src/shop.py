import os
import re

from src.database import Database


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

        # Create mass import
        query = "INSERT INTO adress (zipcode, house_nr, house_nr_addition) VALUES "

        # Loop through string array
        for key, value in lines.items():
            row = value[:-1].split(',')

            # Get adres info
            adresInfo = self.__get_adres_info(row)

            series_index = 1
            if (adresInfo['house_nr'] % 2) == 0:
                # Even
                series_index = 0

            search_zipcode = "SELECT id FROM zipcode WHERE zipcode = '" + adresInfo['zipcode'] + \
                             "' AND series_index = " + series_index + " AND " + adresInfo['house_nr'] + \
                             " BETWEEN breakpoint_from AND breakpoint_to"
            query += "((" + search_zipcode + ")), '" + adresInfo['house_nr'] + "', '" + adresInfo[
                'house_ad'] + "'),"

            # query
            self.db.execute(query[:-1])

        # commit cursor
        self.db.get_connection().commit()

    def __import_restaurant(self, lines):

        # Create mass import
        query = "INSERT INTO restaurant (adress_id, name, phone_nr) VALUES "

        for key, value in lines.items():
            row = value[:-1].split(',')

            # Get adres info
            adresInfo = self.__get_adres_info(row)

            query += "((SELECT id FROM adress WHERE zipcode = '" + adresInfo['zipcode'] + "' AND house_nr = '" + \
                     adresInfo['house_nr'] + "' AND house_nr_addition = '" + adresInfo[
                         'house_ad'] + "'), '" + row[0] + "', " + adresInfo['phone_nr'] + "),"

        self.db.execute(query[:-1])

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
