from sqlalchemy import create_engine

from src.configParser import ConfigParser


class dbEbgine:

    def __init__(self):
        config = ConfigParser().get_config()

        server = config["Server"]
        database = config["Database"]
        username = config["Username"]
        password = config["Password"]

        self.engine = create_engine(f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=SQL Server')

    # Get engine connection
    def get_db_engine(self):
        return self.engine
