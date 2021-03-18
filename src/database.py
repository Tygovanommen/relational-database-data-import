import configparser
import os
import pyodbc

from src.logger import Logger


class Database:
    cursor = conn = None

    def __init__(self):
        config = self.__get_config()
        try:
            self.conn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=' + config["Server"] + ';DATABASE=' + config[
                    "Database"] + ';UID=' + config["Username"] + ';PWD=' + config["Password"])

            self.cursor = self.conn.cursor()
        except pyodbc.Error as ex:
            Logger().error("Something went wrong connecting to database: " + ex.args[1])
            exit()

    # Read config file
    def __get_config(self):
        # Parse file
        config = configparser.ConfigParser()
        config.read(os.getcwd() + "/config.ini")

        # Create array with config values
        values = {}
        values["Server"] = config.get('database', 'Server')
        values["Database"] = config.get('database', 'Database')
        values["Username"] = config.get('database', 'Username')
        values["Password"] = config.get('database', 'Password')

        return values

    def get_connection(self):
        return self.conn

    # Execute query
    def execute(self, query):
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except pyodbc.Error as e:
            error_log = repr(e).split(';')
            for error in error_log:
                print(error)

        except pyodbc.DatabaseError as e:
            print(e)

        except pyodbc.DataError as e:
            print(e)

        except pyodbc.OperationalError as e:
            print(e)
