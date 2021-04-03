import os
from src.database import Database


class Shop:
    # Filename + extension
    filename = None

    # Constructor to setup shop importer
    def __init__(self, filename):
        self.filename = filename

    # Process shop file
    def process(self):
        result = 1
        lines = self.__get_lines()
        if lines:
            result = self.__import_data(lines)
        return result

    # Read data
    def __get_lines(self):
        lines = {}
        i = 0
        with open(os.getcwd() + "/watch/" + self.filename, 'r') as r_file:
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
                lines[i] += line.strip() + ','

            return lines

    # Import data to database
    def __import_data(self, lines):
        db = Database()

        # Create mass import
        query = "INSERT INTO adress (zipcode, house_nr) VALUES "

        # Loop through string array
        for key, value in lines.items():
            row = value[:-1].split(',')
            query += "('" + row[5] + "', '" + row[2] + "'),"

        # Execute query
        print(query[:-1])
        response = db.execute(query[:-1])
        if response:
            return 1
        else:
            return 0
