import pyodbc

from src.configParser import ConfigParser
from src.logger import Logger


class Database:
    cursor = conn = None

    def __init__(self):
        config = ConfigParser().get_config()
        try:
            self.conn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=' + config["Server"] + ';DATABASE=' + config[
                    "Database"] + ';UID=' + config["Username"] + ';PWD=' + config["Password"])

            self.cursor = self.conn.cursor()
        except pyodbc.Error as ex:
            Logger().error("Something went wrong connecting to database: " + ex.args[1])
            exit()

    def get_cursor(self):
        return self.cursor

    def get_connection(self):
        return self.conn

    # Execute query
    def execute(self, query):
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except pyodbc.DataError as e:
            Logger().error(e)
        except pyodbc.OperationalError as e:
            Logger().error(e)
        except pyodbc.DatabaseError as e:
            Logger().error(e)
        except pyodbc.Error as e:
            error_log = repr(e).split(';')
            for error in error_log:
                Logger().error(error)
