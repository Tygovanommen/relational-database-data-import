import configparser
import os
from sqlalchemy import create_engine
from src.database import Database


# Read config file
def __get_config():
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


def get_db_engine():
    config = __get_config()

    server = config["Server"]
    database = config["Database"]
    username = config["Username"]
    password = config["Password"]

    engine = create_engine(
        f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=SQL Server')
    return engine
